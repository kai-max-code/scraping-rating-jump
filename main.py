from glob import glob

def elorating(win_rate, lose_rate, K=32):
    Ea = 1 / (1 + pow(10, (lose_rate-win_rate)/400))
    Eb = 1 / (1 + pow(10, (win_rate-lose_rate)/400))
    new_win_rate = win_rate + K * (1.0 - Ea)
    new_lose_rate = lose_rate + K * (-Eb)
    return new_win_rate, new_lose_rate

def rating(rate_dict, data, date):
    num_data = len(data)
    for i in range(num_data):
        for k in range(i+1, num_data):
            if not data[i][1] in rate_dict:
                rate_dict[data[i][1]] = 1500
            if not data[k][1] in rate_dict:
                rate_dict[data[k][1]] = 1500
            rate_dict[data[i][1]], rate_dict[data[k][1]] = elorating(rate_dict[data[i][1]], rate_dict[data[k][1]])

def delete_null(data):
    delete_ind = []
    rank_dict = {}
    for i in range(len(data)-1, -1, -1):
        if data[i][0] == '休載':
            data.pop(i)
        elif len(data[i]) != 2:
            data.pop(i)
        else:
            data[i][0] = int(data[i][0])

def main():
    data_path_list = glob('data/*.csv')
    data_path_list.sort()
    date_list = []
    for data_name in data_path_list:
        d_l = data_name.replace('data/', '').replace('.csv', '').split('_')
        date_list.append({'year': int(d_l[0]), 'month': int(d_l[1]), 'day': int(d_l[2])})
    print('{}/{}/{} から {}/{}/{} まで \n'.format(date_list[0]['year'], date_list[0]['month'], date_list[0]['day'],
                                                date_list[-1]['year'], date_list[-1]['month'], date_list[-1]['day']))

    rate_dict = {}
    for date in date_list:
        data_path = 'data/{}_{}_{}.csv'.format(date['year'], str(date['month']).zfill(2), str(date['day']).zfill(2))
        f = open(data_path, 'r')
        data = f.read().split('\n')
        data = [i.split(',') for i in data]
        data.pop()

        delete_null(data)
        rating(rate_dict, data, date)

    rate_dict = sorted(rate_dict.items(), key=lambda x: x[1], reverse=True)
    
    print('rank | rate | name')
    for (i, (name, rate)) in enumerate(rate_dict):
        if i < 9:
            print(' {}位 | {:.0f} | {}'.format(i+1, rate, name))
        else:
            print('{}位 | {:.0f} | {}'.format(i+1, rate, name))

if __name__ == '__main__':
    main()
