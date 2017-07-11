#_*_coding:utf-8_*_
from testxpath import myPageStucture
import re
import pickle
import MySQLdb



def deal_response(response):
    thisclass = myPageStucture.pageStructure()

    def getchild(fatherfunc, tagfunc, xpathfunc, numfunc, fatherstructure_class):
        # 1,因为fathernode下边需要有子节点信息,所有传入子getchild中;
        # 2,传来xpathfunc的时候就已经包含了tag信息了;
        # 3,content,

        # thisclass2=myPageStucture.pageStructure()
        fatherstructure_class.content = fatherfunc.xpath('%s[%d]/text()' % (xpathfunc, numfunc)).extract()
        thischild = fatherfunc.xpath('%s[%d]/child::node()' % (xpathfunc, numfunc))
        has_url = fatherfunc.xpath('%s[%d]/@href' % (xpathfunc, numfunc)).extract()
        if has_url:
            fatherstructure_class.has_url = 1
        # fatherstructure_class.Init()#在这里初始化





        #因为要用到father的基本信息,所以在这里来实现
        #-----------------------------------------------------------------从myPageStrcture中的Init方法中拷贝过来的.
        content = ''
        for tl in fatherstructure_class.content:
            fatherstructure_class.TL = len(tl)
            content += tl

        content=content.replace('\r','').replace('\n','').replace('\t','')
        # fatherstructure_class.TL=len(fatherstructure_class.content.pop())#文本长度

        Re_find_symbol = re.compile(ur'[\,\.\'\"\;\。\-\，”“!《》！，\<\>\{\}\<\>]')
        # Re_find_sub_nouse=re.compile(ur'\r')
        PN_list_biaodian = Re_find_symbol.findall(content)  # 所有的标点符号

        fatherstructure_class.PN = len(PN_list_biaodian)

        content_no_Symbol = re.sub(Re_find_symbol, repl='', string=content)  # 没有符号的文本内容
        fatherstructure_class.TL_no_symbol = len(content_no_Symbol)

        fatherstructure_class.All_clause = re.split(Re_find_symbol, content)
        lenth = 0
        for one_clause in fatherstructure_class.All_clause:
            if fatherstructure_class.PN != 0:
                lenth += len(one_clause) / fatherstructure_class.PN
            else:
                lenth += 0
        fatherstructure_class.TAL = lenth  # 这个指标被我给改变了,是我自定义的一个指标
        fatherstructure_class.ND=len(fatherstructure_class.xpath.split('/'))

        #------------------------------------------------------------------


        #-------------------------------------------------------------------
        #添加数据格式化处理模块
        try:
            connect=MySQLdb.connect(host='127.0.0.1', user='root', passwd='asd123456', charset='utf8')
            thiscousor=connect.cursor()
            # if not content:
            #     content='None--None'
            save_page_information='INSERT INTO machineLearning_xpath.xpath_result_1 (name1,num,xpath,content,TL,PN,ND,TAL,TP,has_url,divnum) VALUE ("%s",%d,"%s","%s",%d,%d,%d,%d,"%s",%d,%d)'%(
                fatherstructure_class.name,fatherstructure_class.num,fatherstructure_class.xpath,content.replace('"','_+_'),fatherstructure_class.TL,fatherstructure_class.PN,fatherstructure_class.ND,fatherstructure_class.TAL,
                fatherstructure_class.TP,fatherstructure_class.has_url,fatherstructure_class.divnum
            )
            thiscousor.execute(save_page_information)
            connect.commit()
        except Exception as e:
            print e




        # print '%s[%d]/child::node()' % (xpathfunc, numfunc)#没有蛋用
        # print ' ----------------------------text--begin-----------------------------------'
        # for icontent in fatherfunc.xpath('%s[%d]/text()' % (xpathfunc, numfunc)).extract():
        #     print icontent
        # print '        -----------------------text--end--------------------'

        tag_this_div = {}  # 用一个字典来判断这个子标签div在所在的标签中出现了多少次好用来设置xpath路径
        div_number = 1
        for j2 in thischild:  # 相当于第一层没有处理，是从第二层开始处理的，每一层的信息都在下一层的
            try:
                thisclass2 = myPageStucture.pageStructure()
                tag = j2.root.tag
                xpath = '%s[%d]/%s' % (xpathfunc, numfunc, tag)
                if tag not in tag_this_div.keys():  # 如果这个标签没出现过,记录它,num重置;否则,num+1
                    tag_this_div[tag] = 1
                    num = 1  # 后来发现其实不要这个num也是可以没有的，后边直接传入tag_this_div[tag]
                else:
                    tag_this_div[tag] += 1
                    num = tag_this_div[tag]

                if fatherstructure_class.TP=='A':
                    thisclass2.TP='A'
                else:
                    if thisclass2.name=='a':
                        thisclass2.TP='A'
                    elif thisclass2.name in ['div','tr','td']:
                        thisclass2.TP='D'
                    else:
                        thisclass2.TP='S'


                thisclass2.name = tag
                # thisclass2.content=fatherfunc.xpath('%s[%d]/text()' % (xpathfunc, numfunc)).extract()#传过来就已经是子标签,所以这里处理一下num就行
                thisclass2.num = num
                thisclass2.xpath = xpath
                thisclass2.divnum = div_number
                fatherstructure_class.child[
                    tag + '_' + str(num)] = thisclass2  # 这里的tag貌似没有添加下标，可能会出错。#7-6对头,今天发现了tag没有下表,出错了
                # has_url= fatherfunc.xpath('%s[%d]/@href'%(xpathfunc,numfunc)).extract()
                # if has_url:
                #     thisclass2.has_url=1


                div_number += 1  # 这个div_number代表是的当前子节点下所有的子标签数量，前边的num表示的同一个标签的的出现次数
                getchild(j2, tag, xpath, num, thisclass2)
            except Exception as e:
                print e

    i1 = response.xpath('/child::node()')
    num = 1
    tag_this_div = {}
    div_number = 1
    for j1 in i1:
        try:
            tag = j1.root.tag
            xpath = '/' + tag
            if tag not in tag_this_div.keys():  # 如果这个标签没出现过,记录它,num重置;否则,num+1
                tag_this_div[tag] = 1
                num = 1
            else:
                tag_this_div[tag] += 1
                num = tag_this_div[tag]

            # 所有信息提取完成

            thisclass.name = tag
            thisclass.content = j1.xpath('/%s/text()' % tag).extract()
            thisclass.xpath = xpath
            thisclass.num = 1
            thisclass.divnum = div_number
            # thisclass需要获得5个标签,这里4个,下边在子节点中再获得它所有的child
            # print xpath
            getchild(fatherfunc=j1, tagfunc=tag, xpathfunc=xpath, numfunc=num, fatherstructure_class=thisclass)
            div_number += 1
        except Exception as e:
            pass  # /html/body/div[7]/table/tbody/tr/td[1]/div/table[2]/tbody/tr[2]/td/p/b/font

    # print thisclass
    return thisclass
    # p1 = pickle.dumps(thisclass,
    #                   -1)  # /html/body/div[7]/table/tbody/tr/td[3]/div/table/tbody/tr[1]/td/div/table[3]/tbody/tr/td/p/table/tbody/tr[1]/td[2]
    # file2 = '/media/liang/3804CCCA04CC8C76/project/YFzhongxin/xpath_test/xpath.pkl'
    # with open(file2, 'w+') as fl:
    #     fl.write(p1)
    # pass