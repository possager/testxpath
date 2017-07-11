#_*_coding:utf-8_*_
import pickle
import deal_response
import myPageStucture

file1='/media/liang/3804CCCA04CC8C76/project/YFzhongxin/xpath_test/xpath.pkl'
file1_data=open(file1,'r+')
web_dict=pickle.load(file1_data)
thisclass=deal_response.deal_response(web_dict)
print thisclass