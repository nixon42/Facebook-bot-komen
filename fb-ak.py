import requests
import random
import os
from getpass import getpass
from time import sleep
from bs4 import BeautifulSoup
from threading import Thread

CACHE = '.fb.accnt'  # Cache file akun kalian
WORD = ['login',
        'slurr',    # kata kata buat komen,
        'log',      # nanti diacak biar gak dikira spam dari bot
        'bruhh',
        'tross',
        'loss',
        'masih',
        'kurang',
        'banyak',
        'sepp']
LEGHT = [2, len(WORD)]  # Panjang komen [minimal, maksimal] nanti panjang komen juga random
INTERVAL = 20  # Interval ngirim komen, gak usah cepet cepet biar aman
DELAY = 60  # Setiap 10 kali komen akan ada delay
URL = ''  # Ni setiap kalian buat session, kalian bisa memasukan URL postingan.
# Tapi kalo mau URL dari postingan static, tinggal ganti dengan URL tsb.


class Facebook:
    """
    Facebook class
    """

    def __init__(self):
        """
        Facebook class
        """
        self.session = requests.session()
        self.url = 'https://m.facebook.com'

    def login(self, cache):
        """
        Login into Facebook
        :param cache: The account cache file
        :return: none
        """

        def get_data():
            """
            Get data that required for login
            :return: Tuple { Data Dictionary , A }
            """
            data = {}
            act_url = ''
            log_in = self.session.get(self.url)
            if log_in.ok:
                lpage = BeautifulSoup(log_in.content, 'lxml')

                form = lpage.find('form', {'id': 'login_form'})
                trash = form.find('input', {'name': 'sign_up'})
                inpt = form.find_all('input')

                act_url = form.get('action')

                inpt.remove(trash)

                i = 0
                while i < len(inpt):
                    try:
                        data[inpt[i]['name']] = inpt[i]['value']
                    except:
                        if not os.path.exists(cache):
                            cache_file = open(cache, 'a+')
                            email = input('E-Mail : ')
                            password = getpass('Password : ')
                            cache_file.write(email + '\n')
                            cache_file.write(password)
                        else:
                            cache_file = open(cache, 'r')
                            lines = cache_file.readlines()
                            email = lines[0]
                            password = lines[1]

                        if inpt[i]['name'] == 'email':
                            inpt[i]['value'] = email
                        elif inpt[i]['name'] == 'pass':
                            inpt[i]['value'] = password
                        i -= 1
                    i += 1
            else:
                os.system('rm ' + cache)
                print('Gagal menghubungi fb')
                print('Cek koneksi')
                sleep(1)
                print('Mencoba dalam 3 detik ', end='')
                for _ in range(3):
                    print('. ', end='')

                get_data()

            return data, act_url

        def login():
            """
            Login into facebook with url and data
            :return: none
            """
            data, act_url = get_data()
            self.session.post(self.url + act_url, data)

        def check():
            """
            Check if login attemp is successfull
            :return: Name of the account
            """
            pro_url = 'https://mobile.facebook.com/profile.php'
            r = self.session.get(pro_url)

            profile = BeautifulSoup(r.content, 'lxml')

            root = profile.find('div', {'id': 'root'})
            name = root.find('strong').text

            if name == '':
                print('Log in Unsuccessful')
                return None
            else:
                print('\n')
                print('Login Success....')
                print('Acccount : ' + name)
                print('')
                print('')
                return name

        if __name__ == '__main__':
            login()
            check()

    def komen(self, post, komen):
        pst = self.session.get(post)
        soup = BeautifulSoup(pst.content, 'lxml')
        form = soup.find('form')
        inpt = form.findAll('input', {'type': 'hidden'})

        data = {}
        for ip in inpt:
            data[ip['name']] = ip['value']

        data['comment_text'] = komen
        act_url = form.get('action')

        self.session.post(self.url + act_url, data)
        print('Postingan : ', soup.find('title').text)
        print('Komentar : ', komen)


class Generate:
    def __init__(self, word):
        self.word = word

    def gen_word(self, much):
        words = ''
        for _ in range(much):
            words += ' ' + random.choice(self.word)

        return words


if __name__ == '__main__':
    print('------ BOT FB AUTO KOMEN ------')
    print('By : NiXoN 42')
    print('Github : https://github.com/nixon42')
    print('\n')
    print('\n')
    gen = Generate(WORD)
    fb = Facebook()
    fb.login(CACHE)

    print('========= MULAI ==============')
    if URL == '':
        url = input('URL POSTINGAN : ')
    else:
        url = URL
    print('\n')

    while True:
        try:
            req = requests.session().get(url)
            break
        except:
            print('URL yang anda masukan mungkin salah')
            print('Atau mungkin koneksi anda sedang bermasalah')
            sleep(1)
            url = ('URL : ')

    jlh_komen = 0
    lst = []
    while True:
        if len(lst) < 10:
            lst.append(gen.gen_word(random.randrange(LEGHT[0], LEGHT[1])))
        else:
            for k in lst:
                try:
                    Thread(target=fb.komen, args=(url, k)).start()
                    jlh_komen += 1
                    print('jumlah komen : ', jlh_komen.__str__())
                    print('\n')
                    sleep(INTERVAL)
                except:
                    print('Gagal menghubungi fb')
                    print('Cek koneksi')
                    sleep(1)
                    print('Mencoba dalam 3 detik ', end='')
                    for _ in range(3):
                        print('. ', end='')

            sleep(DELAY)
