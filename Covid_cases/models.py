from django.db import models

# Create your models here.
class Cases(models.Model):
    total_confirmed = models.IntegerField()
    total_recovered = models.IntegerField()
    total_deaths = models.IntegerField()
    newly_confirmed = models.IntegerField()
    newly_deaths = models.IntegerField()
    active_cases = models.IntegerField()

    def __str__(self):
        return "{total_confirmed:"+str(self.total_confirmed)+","+"total_recovered:"+str(self.total_recovered)+","+"total_deaths:"+str(self.total_deaths)+","+"newly_confirmed:"+str(self.newly_confirmed)+","+"newly_deaths:"+str(self.newly_deaths)+","+"active_cases:"+str(self.active_cases)+"}"


class Country(models.Model):
    country_name = models.CharField(max_length=50)
    cases = models.OneToOneField(Cases, on_delete=models.CASCADE)

    def __str__(self):
        # return self.country_name
        # return "{name:"+self.country_name+","+"total_confirmed:"+str(self.cases.total_confirmed)+","+"total_recovered:"+str(self.cases.total_recovered)+","+"total_deaths:"+str(self.cases.total_deaths)+","+"newly_confirmed:"+str(self.cases.newly_confirmed)+","+"newly_deaths:"+str(self.cases.newly_deaths)+","+"active_cases:"+str(self.cases.active_cases)+"}"
        # return "{total_confirmed:"+str(self.cases.total_confirmed)+","+"total_recovered:"+str(self.cases.total_recovered)+","+"total_deaths:"+str(self.cases.total_deaths)+","+"newly_confirmed:"+str(self.cases.newly_confirmed)+","+"newly_deaths:"+str(self.cases.newly_deaths)+","+"active_cases:"+str(self.cases.active_cases)+"}"
        return "{'total_confirmed':"+str(self.cases.total_confirmed)+","+"'total_recovered':"+str(self.cases.total_recovered)+","+"'total_deaths':"+str(self.cases.total_deaths)+","+"'newly_confirmed':"+str(self.cases.newly_confirmed)+","+"'newly_deaths':"+str(self.cases.newly_deaths)+","+"'active_cases':"+str(self.cases.active_cases)+"}"
        # return '''{"total_confirmed":'''+str(self.cases.total_confirmed)+''','''+'''"total_recovered":'''+str(self.cases.total_recovered)+''','''+'''"total_deaths":'''+str(self.cases.total_deaths)+''','''+'''"newly_confirmed":'''+str(self.cases.newly_confirmed)+''','''+'''"newly_deaths":'''+str(self.cases.newly_deaths)+''','''+'''"active_cases":'''+str(self.cases.active_cases)+'''}'''
