from django.contrib.auth.models import AbstractUser, User
from django.utils.text import slugify
#from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from yahoofinancials import YahooFinancials
from django.core.validators import MaxValueValidator

User = settings.AUTH_USER_MODEL

class CustomUser(AbstractUser):
    def __str__(self):
        return self.email

# class Sell(models.Model):
#     sell_price = models.DecimalField(blank=True,max_digits=10,decimal_places=2)
#     sell_date = models.DateField(blank=True)
#     sell_quant = models.DecimalField(blank=True,max_digits=10,decimal_places=2)


class Stock(models.Model):
    stock_name = models.CharField(max_length=100)
    stock_date = models.DateField()
    stock_quant = models.DecimalField(max_digits=10, decimal_places=2)
    stock_currency = models.CharField(max_length=10)
    stock_cb = models.DecimalField(max_digits=10, decimal_places=2)
    stock_final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(null=True,max_digits=10,decimal_places=2)
    sell_date = models.DateField(null=True)
    sell_quant = models.DecimalField(null=True,max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(User, default=1 ,on_delete=models.CASCADE)

    @property
    def get_stock_cb(self):
        now = self.stock_date
        today = now.strftime("%Y-%m-%d")
        yahoo_financials = YahooFinancials(self.stock_name)
        cb = yahoo_financials.get_historical_price_data(today, today, 'weekly')
        final_cb=round(cb[self.stock_name]['prices'][0]['close'],2)
        cb = final_cb
        return cb

    # @property
    # def get_final_invested_amount(self):
    #     now = self.stock_date
    #     today = now.strftime("%Y-%m-%d")
    #     yahoo_financials = YahooFinancials(self.stock_name)
    #     cb = yahoo_financials.get_historical_price_data(today, today, 'weekly')
    #     final_cb=round(cb[self.stock_name]['prices'][0]['close'],2)
    #     final = final_cb*float(self.stock_quant)
    #     return final

    def save(self):
        self.stock_cb = self.get_stock_cb
        self.stock_final_amount = self.get_stock_cb*float(self.stock_quant)
        self.slug = slugify(self.stock_name + '-' + (self.stock_date).strftime("%Y-%m-%d") + '-' + str(self.user_id))
        super(Stock, self).save()
