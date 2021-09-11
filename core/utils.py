from datetime import date as dt
from bs4 import BeautifulSoup
import requests
from django.shortcuts import render
import plotly
import plotly.graph_objs as plt
from plotly.offline import plot
from django.utils.safestring import mark_safe
from .models import CategoryModel


def rate_now(data):
    categories = CategoryModel.objects.all()
    data['categories'] = categories
    date = str(dt.today()).split('-')
    date = date[2] + '/' + date[1] + '/' + date[0]
    try:
        soup = BeautifulSoup(requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}').content, 'xml')
        data['usd'] = soup.find('CharCode', text='USD').find_next_sibling('Value').string + ' руб'
        data['eur'] = soup.find('CharCode', text='EUR').find_next_sibling('Value').string + ' руб'
    except AttributeError:
        return data
    return data


class DataMixin:
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = CategoryModel.objects.all()
        context['categories'] = categories
        today_rate = self.get_today_rate()
        return dict(list(context.items()) + list(today_rate.items()))

    def get_today_rate(self):
        context = {}
        date = str(dt.today()).split('-')
        date = date[2] + '/' + date[1] + '/' + date[0]
        try:
            soup = BeautifulSoup(requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}').content,
                                 'xml')
            context['usd'] = soup.find('CharCode', text='USD').find_next_sibling('Value').string + ' руб'
            context['eur'] = soup.find('CharCode', text='EUR').find_next_sibling('Value').string + ' руб'
        except AttributeError:
            return context
        return context

    def get_context_rate(self, request, context):
        date, currency = request.POST.get('date'), request.POST.get('currency').split(', ')
        date = date[8:] + '/' + date[5:7] + '/' + date[:4]
        soup = BeautifulSoup(requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}').content, 'xml')
        try:
            context['result'] = f'Курс {currency[1]} по состоянию на {date} - ' + \
                                soup.find('CharCode', text=currency[0]).find_next_sibling('Value').string + ' руб'
        except Exception:
            context['result'] = 'Извините, такой информации не было найдено на сайте ЦБ РФ'
        return render(request, 'core/rate.html', context)

    def get_context_bik(self, request, context):
        bik = request.POST.get('bik')
        soup = BeautifulSoup(requests.get(f'https://www.cbr.ru/scripts/XML_bic.asp?bic={bik}').content, 'xml')
        try:
            context['result'] = f'Наименование кредитной организации с БИК №{bik} - ' + soup.find('ShortName').string
        except Exception:
            context['result'] = 'Извините, организация с таким БИК не была найдена'
        return render(request, 'core/bik.html', context)

    def get_context_currency_dynamic(self, request, context):
        currency, start_date, end_date = request.POST.get('currency').split(', '), request.POST.get('start_date'), \
                                         request.POST.get('end_date')

        start_date = start_date[8:] + '/' + start_date[5:7] + '/' + start_date[:4]
        end_date = end_date[8:] + '/' + end_date[5:7] + '/' + end_date[:4]
        soup = BeautifulSoup(requests.get(f'https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={start_date}'
                                          f'&date_req2={end_date}&VAL_NM_RQ={currency[2]}').content, 'xml')
        try:
            dates = [i['Date'] for i in soup.find_all('Record')]
            values = [float(i.string.replace(',', '.')) for i in soup.find_all('Value')]
            my_plot_div = plot(
                {'data': [plt.Scatter(x=dates, y=values, line=dict(color="#0bd94f"))],
                 "layout": plt.Layout(title=f'График курса {currency[1]} с {start_date} по {end_date}',
                                      xaxis_title="Даты", yaxis_title="Курс в рублях")},
                output_type='div'
            )
            context['text'] = 'Ваш график:'
            context['result'] = mark_safe(my_plot_div)
        except Exception:
            context['result'] = 'Извините, такой информации не было найдено на сайте ЦБ РФ'
        return render(request, 'core/currency_dynamic.html', context)

    def get_context_precious_metals(self, request, context):
        metal, start_date, end_date = request.POST.get('metal').split(', '), request.POST.get('start_date'), \
                                      request.POST.get('end_date')
        start_date = start_date[8:] + '/' + start_date[5:7] + '/' + start_date[:4]
        end_date = end_date[8:] + '/' + end_date[5:7] + '/' + end_date[:4]
        soup = BeautifulSoup(requests.get(
            f'https://www.cbr.ru/scripts/xml_metall.asp?date_req1={start_date}&date_req2={end_date}').content, 'xml')
        try:
            dates = [i['Date'] for i in soup.find_all('Record') if i['Code'] == metal[0]]
            values_buy = [float(i.find('Buy').string.replace(',', '.'))
                          for i in soup.find_all('Record') if i['Code'] == metal[0]]
            values_sell = [float(i.find('Sell').string.replace(',', '.'))
                           for i in soup.find_all('Record') if i['Code'] == metal[0]]
            figure = plt.Figure()
            figure.add_trace(plt.Scatter(x=dates, y=values_buy, line=dict(color="#0bd94f"), name='Цена покупки'))
            figure.add_trace(plt.Scatter(x=dates, y=values_sell, line=dict(color="#e01028"), name='Цена продажи'))
            figure.update_layout(title=f'График курса {metal[1]} с {start_date} по {end_date}',
                                 xaxis_title="Даты", yaxis_title="Курс в рублях", )
            my_plot_div = plotly.io.to_html(figure, full_html=False)
            context['result'] = mark_safe(my_plot_div)
            context['text'] = 'Ваш график:'
        except Exception:
            context['result'] = 'Извините, такой информации не было найдено на сайте ЦБ РФ'
        return render(request, 'core/precious_metals.html', context)
