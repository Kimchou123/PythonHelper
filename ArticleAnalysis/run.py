import nltk
import model.m_mssql as db
import model.translate as fy
import time
from nltk.tokenize import sent_tokenize, word_tokenize
from bs4 import BeautifulSoup
#from googletrans import Translator

EXAMPLE_TEXT = "<p><span style='font-weight: bold;'>How much do you know about Albert Einstein?</span><br>Albert Einstein, born on March 14, 1879 in Germany, was a great scientist in the world. He was strange because he hated haircuts and new clothes. He believed in peace. All his life, he hated war. However, his most<br>famous idea, E = mc², helped create the world’s most dangerous weapon (武<br>器). Many people think he was the smartest person in the world. But Einstein said that he thought like a child with many questions and unusual ideas.<br><span style='font-weight: bold;'>What did he like?</span><br>Einstein liked learning sailing(帆船运 动). He sailed in small boats all his life.  He<br>once joked, “Sailing is the sport that takes the least energy!”<br>When Einstein was a child, his mother made him take violin lessons. At first, he didn’t like the violin. But then he learned to love music and became a good violinist.<br>Later, he said, “Love is the best teacher.”<br><span style='font-weight: bold;'>Why is the sky blue?</span><br>In 1910, Einstein asked a question which many children often ask, “Why is the sky blue?” After his careful research, he answered the question like<br>this: “It’s because light is made up of many colors including blue. When light travels to Earth, gas particles(气体微粒) spread the blue light all over the sky.” His answer is true in physics.</p>"
#for sentence in sent_tokenize(EXAMPLE_TEXT):

# 设置Google翻译服务地址
#translator = Translator(service_urls=[
#      'translate.google.cn'
#    ])
# 翻译成中文

conn = db.get_connection();
#print(conn);
sql = 'select top 1000 id,body from Tb_Article where Id>100756 order by Id';
index1 = 0;
index2 = 3;
params = (index1, index2);
rows = db.execute_query(sql, params);
output_data = open('out.txt', 'w+', encoding='utf=8')
for row in rows:
        html = str(row[1]);
        html = html.replace("&nbsp;","");
        soup = BeautifulSoup(html,'lxml');
        #s= soup.get_text();
        #s= s.replace("\n", "<br/>");
        #s= s.replace("\r", "<br/>");
        #s= s.replace("\"", "'");
        #s= db.filter_tags(str(row[1]));
        s = soup.find_all('p');        
        k=0;
        for p in s:
                text = p.get_text();                
                r = BeautifulSoup(text,'html.parser');
                result = r.get_text(); 
                result= result.replace("\n", "");
                result= result.replace("\r", "");
                #print(result);
                k+=1;
                i=1;
                for sentence in sent_tokenize(result):
                    ss= db.transferContent(sentence);
                    #ch =db.youdao(ss);
                    #dst = translator.translate(ss, dest='zh-CN')
                    #ch = dst.text
                    ch=fy.translate(ss, target='zh-CN')
                    #cursor = conn.cursor();
                    sql = "insert into Tb_ArticleSentence1(ArticleId,Number,Section,Sentence,ChSentence) values({0},{1},{2},'{3}','{4}')".format(row[0],i,k,ss,ch);
                    print(sql);
                    output_data.write(sql + '\n')
                    #cursor.execute(sql);
                    #conn.commit();            
                    #cursor.close();
                    i+=1;
output_data.close()
db.close_connection(conn);
print('mssql is ok');


