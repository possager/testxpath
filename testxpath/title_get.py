import pickle


file1='/media/liang/3804CCCA04CC8C76/project/YFzhongxin/xpath_test/xpath.pkl'
file1_data=open(file1,'r+')
web_dict=pickle.load(file1_data)
# for i in web_dict.child.keys():
#     if i.name=='title':
#         print 'Find it!!  xpath is --------',i.xpath





def getchild(pickle_dict):#这里的pickledict就是一个字典.
    if pickle_dict.name=='title':
        try:
            title_in_getchild=pickle_dict.content.pop()
            print 'find it! the title is ------',title_in_getchild,'the xpath is -----------',pickle_dict.xpath
            return title_in_getchild
        except Exception as e:
            print e
    else:
        for one_key in pickle_dict.child.keys():
            title_in_getchild=getchild(pickle_dict.child[one_key])
            if title_in_getchild:
                return title_in_getchild
        # return title_in_getchild




def dealcontent(webpage_class):
    content=webpage_class.content
    for content_num in range(len(content)):
        content[content_num]=content[content_num].lstrip('\t').lstrip('\n').lstrip(' ').lstrip('\r').rstrip('\t').rstrip('\n').rstrip(' ').rstrip('\r')

    # content=content.strip('\t').strip('\n').strip(' ')
    webpage_class.contetnt=content
    for one_key in webpage_class.child.keys():
        dealcontent(webpage_class.child[one_key])


def find_compare_list(title_str,webpage_class,maybe_content_list):
    this_content_len=len(title_str)
    for one_content in webpage_class.content:
        if len(one_content)<=this_content_len+2 and len(one_content)>5:
            if webpage_class.has_url==0:
                maybe_content_list.append({one_content:webpage_class.xpath})

    for one_key in webpage_class.child.keys():
        find_compare_list(title_str,webpage_class.child[one_key],maybe_content_list)
    return maybe_content_list,title_str


def find_compare_title(title,webpage_class,maybe_content_list=[]):
    maybe_content_list,title_str=find_compare_list(title_str=title,webpage_class=webpage_class,maybe_content_list=maybe_content_list)
    for one_content in maybe_content_list:
        if one_content.keys()[0] in title_str:
            index_in_for=title_str.index(one_content.keys()[0])
            print index_in_for
            if index_in_for<1:
                print 'find it ,------------------the title is (in find_compare_title)-------',one_content.keys()[0]
                print 'the xpath is ',one_content.values()[0]
                print index_in_for

dealcontent(web_dict)
title_str=getchild(web_dict)
find_compare_title(title=title_str,webpage_class=web_dict)
print 'finish'