# -*- coding: UTF-8 -*-

from django.db import models

# Create your models here.


class Person(models.Model):
	student_number = models.CharField(verbose_name = '学号', max_length = 12, unique = True)
	name = models.CharField(verbose_name = '姓名', max_length = 10)
	pinyin = models.CharField(verbose_name = '拼音', max_length = 25)
	gender = models.CharField(verbose_name = '性别', choices = (('F', 'Female'), ('M', 'Male')), max_length = 2)
	native_province = models.CharField(verbose_name = '籍贯', max_length = 10, blank = True)
	dormitory = models.CharField(verbose_name = '寝室', blank = True, max_length = 7)
	birthday = models.DateField(verbose_name = '生日', blank = True)
	phone_number = models.CharField(verbose_name = '手机号码', max_length = 11, blank = True)
	position = models.CharField(verbose_name = '职务', max_length = 20, blank = True)
	participation = models.PositiveSmallIntegerField(verbose_name = '活动参与分', default = 0)

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name


class Activity(models.Model):
	name = models.CharField(verbose_name = '活动名称', max_length = 30)
	date = models.DateField(verbose_name = '日期', blank = True)
	time = models.TimeField(verbose_name = '开始时间', blank = True)
	place = models.CharField(verbose_name = '地点', max_length = 15, blank = True)
	content = models.TextField(verbose_name = '内容', blank = True)
	participation = models.SmallIntegerField(verbose_name = '参与得分', default = 0)
	participator = models.TextField(verbose_name = '参与者学号', blank = True)
	images = models.TextField(verbose_name = '相关图片urls', blank = True)

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name


class Feedback(models.Model):
	summary = models.TextField(verbose_name = '反馈总结', max_length = 50)
	details = models.TextField(verbose_name = '详细信息', max_length = 500, blank = True)
	category = models.CharField(verbose_name = '反馈分类', choices = (('A', 'Advice'), ('B', 'Bug')),
								max_length = 2, default = 'B')
	contact = models.EmailField(verbose_name = '联系邮箱')

	def __unicode__(self):
		return self.summary

	def __str__(self):
		return self.summary


class Finance(models.Model):
	"""
	班费的单次记录
	"""
	income = models.FloatField(verbose_name = '收入', default = 0)
	expense = models.FloatField(verbose_name = '支出', default = 0)
	date = models.DateField(verbose_name = '日期')
	event = models.TextField(verbose_name = '相关事件')
	details = models.TextField(verbose_name = '详细信息', blank = True)

	def __unicode__(self):
		return '%s +%.2f -%.2f' % (self.event, self.income, self.expense)
		# return '{} +{:.2f}, -{:.2f}'.format(self.event.encode('utf-8'), self.income, self.expense).encode('utf-8')

	def __str__(self):
		return '%s +%.2f -%.2f' % (self.event, self.income, self.expense)
		# return '{} +{:.2f}, -{:.2f}'.format(self.event.encode('utf-8'), self.income, self.expense).encode('utf-8')

