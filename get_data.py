from bs4 import BeautifulSoup
import requests
import csv
import time

def main():

    max_pages = 20

    for i in range(max_pages):
        if i == 0:
            url = 'https://jumpranking.blog.fc2.com/page.html'
        else:
            url = 'https://jumpranking.blog.fc2.com/page-{}.html'.format(i)
        get_data(url)
        time.sleep(10)

def get_data(url):
    result = requests.get(url)
    c = result.content
    
    soup = BeautifulSoup(c, 'html.parser')
    
    summary = soup.find_all(["td", "th"])
    date = soup.find_all("p", {'class': 'entry_date'})
    flag = False
    result_list = []
    for i in range(len(summary)):
        summary[i] = str(summary[i]).replace('<td>', '').replace('</td>', '').replace('<th>', '').replace('</th>', '').replace('<a href="http://onepiecedb.web.fc2.com/">', '').replace('</a>', '')
    
        if flag:
            r_list.append(summary[i])
    
        if summary[i] == '前回比較':
            flag = True
            r_list = []
        elif summary[i] == '平均':
            r_list.pop()
            r_list.pop()
            result_list.append(r_list)
            flag = False
            
    for i in range(len(result_list)):
        write_list = []
        for k in range(int(len(result_list[i])/3)):
            write_list.append([result_list[i][3*k], result_list[i][3*k+1]])
        print(write_list)
        date[i] = str(date[i]).replace('<p class="entry_date">', '').replace('</p>', '').replace('/', '_')
        f = open('data/' + str(date[i]) + '.csv', 'w')
        writer = csv.writer(f)
        writer.writerows(write_list)

if __name__ == '__main__':
    main()

