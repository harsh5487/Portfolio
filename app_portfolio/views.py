from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, render_to_response
# from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from . forms import StockForm, SellForm
from . models import Stock
#from django.contrib import messages
from django.contrib.auth.decorators import login_required
from yahoofinancials import YahooFinancials
from django.views.generic import TemplateView
# from django.views.decorators.cache import cache_page


@login_required
def homepage(request):
	if request.method == 'POST':
		form = StockForm(request.POST or None)
		if form.is_valid():
			# def check(ticker,dat):
			# 	cb = yahoo_financials.get_historical_price_data(dat, dat, 'weekly')
			# 	final_cb=round(cb[ticker]['prices'][0]['close'],2)
			# 	return final_cb

			ticker=request.POST.get('stock_name', None)
			yahoo_financials = YahooFinancials(ticker)
			dat=request.POST.get('stock_date', None)
			cb = yahoo_financials.get_historical_price_data(dat, dat, 'weekly')
			curr_ency = cb[ticker]['currency']
			final_cb=round(cb[ticker]['prices'][0]['close'],2)
			quant=int(request.POST.get('stock_quant', None))
			final = final_cb*quant
			cb=final_cb
			data=final
			obj = form.save(commit=False)
			obj.user = request.user
			obj.stock_currency = curr_ency
			obj.save()
			#messages.success(request, ('Stock is added!'))
			form = StockForm()
			stocks = Stock.objects.filter(user=request.user)
			#messages.success(request, ('Stock is added!'))
			return redirect('homepage')
			# return render(request,'stocks.html',{ 'stocks':stocks, 'cb':cb, 'data':data })
	else:
		form = StockForm()
		stocks = Stock.objects.filter(user=request.user)
		return render(request, 'homepage.html', {'form':form, 'stocks':stocks})

# @login_required
# def stocks(request):
# 	stocks = Stock.objects.filter(user=request.user)
# 	return render(request, 'stocks.html', {'stocks':stocks})

@login_required
def details(request, slug):
	stocks = Stock.objects.filter(slug=slug).first()
	name = stocks.stock_name
	date = stocks.stock_date
	quant = stocks.stock_quant
	p_price = stocks.stock_cb
	slug = slug
	yahoo_financials = YahooFinancials(name)
	gain_loss = round(yahoo_financials.get_current_percent_change()*100,3)
	return render(request, 'details.html',{'slug':slug, 'name':name, 'date':date, 'quant':quant, 'p_price':p_price, 'gain_loss':gain_loss})
	#return render(request,'details.html')


@login_required
def get_data(request, slug):
	item = Stock.objects.filter(slug=slug)
	for i in item:
		ticker = i.stock_name
		purchased_price = float(i.stock_cb)
		quantity = float(i.stock_quant)
	yahoo_financials = YahooFinancials(ticker)
	prev_close_balance = yahoo_financials.get_current_price()
	# total = prev_close_balance*quantity
	diff = round(quantity*(prev_close_balance-purchased_price),2)
	default_items = [purchased_price, prev_close_balance, diff]
	data = {
		"default": default_items,
		"difference": diff
	}
	return JsonResponse(data)

def delete(request, slug):
	item = Stock.objects.filter(slug=slug)
	item.delete()
	# messages.success(request,('Stock is deleted!'))
	return redirect('homepage')

def edit(request, slug):
	stock = Stock.objects.filter(slug=slug).first()
	form = StockForm(request.POST or None, instance=stock)
	if form.is_valid():
		obj = form.save(commit=False)
		obj.save()
		form = StockForm()
	return render(request, 'edit.html', {'slug':slug, 'form':form})

def sell(request, slug):
	if request.method == 'POST':
		stock = Stock.objects.filter(slug=slug).first()
		form = SellForm(request.POST or None, instance=stock)
		if form.is_valid():
			obj = form.save(commit=False)
			if stock.sell_quant <= stock.stock_quant:
				stock.stock_quant = stock.stock_quant - stock.sell_quant
				obj.save()
				return redirect('homepage')
			else:
				stock.sell_quant = 0
				obj.save()
				return redirect('homepage')
	else:
		stock = Stock.objects.filter(slug=slug).first()
		if stock.stock_quant <= 0:
			form=""
		else:
			form = SellForm()
		return render(request, 'sell.html', {'form':form, 'stock':stock})

def balance_sheet_data(request):
	stocks = Stock.objects.filter(user=request.user)
	total_amount = 0
	label_list = []
	b_data = []
	for i in stocks:
		total_amount += i.stock_final_amount
		label_list.append(i.stock_name)
		b_data.append(float(i.stock_final_amount))

	data = {
		"labels": label_list,
		"data_balance": b_data,
		"total": total_amount
	}
	return JsonResponse(data)

@login_required
def balance_sheet(request):
	stocks = Stock.objects.filter(user=request.user)
	total = 0
	latest = 0
	loss_profit = 0
	percent = 0
	for stock in stocks:
		total += float(stock.stock_final_amount)
		ticker = stock.stock_name
		t = YahooFinancials(ticker)
		latest += float(round(t.get_current_price(),2)*float(stock.stock_quant))
	loss_profit = round(abs(float(total)-latest),2)
	try:
		percent = ((latest - total)/latest)*100
	except Exception as e:
		pass
	return render(request,'balance.html', {'stocks': stocks, 'total':total, 'latest':round(latest,2), 'loss_profit':loss_profit, 'percent': round(percent,2)})
