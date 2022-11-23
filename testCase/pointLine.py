# coding=utf-8
import json
import re


def transform_json(line):
    point_list = line.split(',')
    value = []
    for i in point_list:
        point = i.split(' ')
        value.append({'lat': float(point[1]), 'lon': float(point[0])})
    print(value)
    return value


def transform_lonlat(str_line):
    latlon_str = ''
    re_lon = '"lon":(\d+.?\d+)'
    re_lat = '"lat":(\d+.?\d+)'
    match_lon = re.findall(re_lon, str_line)
    match_lat = re.findall(re_lat, str_line)
    if match_lon and match_lat:
        if len(match_lon) == len(match_lat):
            for i in range(0, len(match_lon)):
                if i != len(match_lon) - 1:
                    latlon_str += match_lon[i] + ' ' + match_lat[i] + ','
                else:
                    latlon_str += match_lon[i] + ' ' + match_lat[i]
        print(latlon_str)
    else:
        print('输入内容无效')


def transForString(str1: str):
    trans_str = str1.replace('\"', "\\\"")
    print(trans_str)


if __name__ == '__main__':

    # str转json
    # 支持格式: lon lat
    # 返回结果：{'lat': , 'lon':}
    # json_str = transform_json('104.02679443359375 1.2695036575539094,104.27398681640625 1.2770548931316255,104.3756103515625 1.3429556294180167,104.5294189453125 1.5433924157292807,104.60906982421875 1.7383196831793803,104.65850830078125 1.8700902342355095,104.70794677734375 2.0265548563992843,104.8040771484375 2.191238104506552,104.996337890625 2.4217639236659676,104.974365234375 2.67419944615503,105.040283203125 2.8497764266656023,105.1171875 3.069209801857123,105.3643798828125 3.3982743902097345,105.5621337890625 3.6340356301913808,105.677490234375 3.908098881894123,105.8367919921875 4.110848398717305,105.97412109375 4.269724272266757,106.1114501953125 4.417613653658063,106.4190673828125 4.614753461811727,106.5179443359375 4.724252074523264,106.6552734375 4.844680562025371,106.7047119140625 4.888467448761478')
    # str_json = json.dumps(json_str)

    # 从json中获取具体的 str
    # 支持格式：含"lat":、"lon":的数据
    # 返回结果: lon lat
    transform_lonlat('{"code":"","data":{"routePoints":null,"restPointsOnLine":[{"mmsi":235068031,"lon":119.75559491742978,"lat":22.622713574814934,"posDate":null,"seqNo":1},{"mmsi":235068031,"lon":119.746948,"lat":22.640133,"posDate":null,"seqNo":2},{"mmsi":235068031,"lon":119.73885,"lat":22.655283,"posDate":null,"seqNo":3},{"mmsi":235068031,"lon":119.683723,"lat":22.76985,"posDate":null,"seqNo":4},{"mmsi":235068031,"lon":119.59932,"lat":22.917685,"posDate":null,"seqNo":5},{"mmsi":235068031,"lon":119.556152,"lat":22.969433,"posDate":null,"seqNo":6},{"mmsi":235068031,"lon":119.459236,"lat":23.08575,"posDate":null,"seqNo":7},{"mmsi":235068031,"lon":119.37987,"lat":23.1822,"posDate":null,"seqNo":8},{"mmsi":235068031,"lon":119.282265,"lat":23.29695,"posDate":null,"seqNo":9},{"mmsi":235068031,"lon":119.19952,"lat":23.389383,"posDate":null,"seqNo":10},{"mmsi":235068031,"lon":119.06495,"lat":23.511116,"posDate":null,"seqNo":11},{"mmsi":235068031,"lon":118.996735,"lat":23.572582,"posDate":null,"seqNo":12},{"mmsi":235068031,"lon":118.95708411965397,"lat":23.608397202407197,"posDate":null,"seqNo":13},{"mmsi":235068031,"lon":118.88841365711819,"lat":23.67063620355671,"posDate":null,"seqNo":14},{"mmsi":235068031,"lon":118.8289,"lat":23.72535,"posDate":null,"seqNo":15},{"mmsi":235068031,"lon":118.806817,"lat":23.74665,"posDate":null,"seqNo":16},{"mmsi":235068031,"lon":118.68985,"lat":23.855583,"posDate":null,"seqNo":17},{"mmsi":235068031,"lon":118.619983,"lat":23.919267,"posDate":null,"seqNo":18},{"mmsi":235068031,"lon":118.597483,"lat":23.93975,"posDate":null,"seqNo":19},{"mmsi":235068031,"lon":118.510133,"lat":24.019517,"posDate":null,"seqNo":20},{"mmsi":235068031,"lon":118.413817,"lat":24.107517,"posDate":null,"seqNo":21},{"mmsi":235068031,"lon":118.399717,"lat":24.12455,"posDate":null,"seqNo":22},{"mmsi":235068031,"lon":118.402917,"lat":24.144,"posDate":null,"seqNo":23},{"mmsi":235068031,"lon":118.406883,"lat":24.150917,"posDate":null,"seqNo":24},{"mmsi":235068031,"lon":118.408867,"lat":24.1672,"posDate":null,"seqNo":25},{"mmsi":235068031,"lon":118.392467,"lat":24.152767,"posDate":null,"seqNo":26},{"mmsi":235068031,"lon":118.361767,"lat":24.089133,"posDate":null,"seqNo":27},{"mmsi":235068031,"lon":118.362383,"lat":24.098717,"posDate":null,"seqNo":28},{"mmsi":235068031,"lon":118.365067,"lat":24.105469,"posDate":null,"seqNo":29},{"mmsi":235068031,"lon":118.36565,"lat":24.161367,"posDate":null,"seqNo":30},{"mmsi":235068031,"lon":118.33605,"lat":24.181017,"posDate":null,"seqNo":31},{"mmsi":235068031,"lon":118.25965,"lat":24.2448,"posDate":null,"seqNo":32},{"mmsi":235068031,"lon":118.203467,"lat":24.306783,"posDate":null,"seqNo":33},{"mmsi":235068031,"lon":118.101717,"lat":24.402867,"posDate":null,"seqNo":34},{"mmsi":235068031,"lon":117.998167,"lat":24.44575,"posDate":null,"seqNo":35},{"mmsi":235068031,"lon":117.984817,"lat":24.44815,"posDate":null,"seqNo":36}]}}')
