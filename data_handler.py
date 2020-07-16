import requests
from bs4 import BeautifulSoup
import pandas as pd
from email_sender import EmailSender


class HandlerDataFrame:
    """This class gets input data and handles them
    
    Parameters
    --------------
    urls: list - currency urls
    """
    
    def __init__(self, urls: list):
        self.urls = urls
        self.data = pd.DataFrame()

    def handle_data(self):
        """For every currency we create DF.After that is added new coll diff"""

        for current in self.urls:
            temp_df = pd.DataFrame(current, columns=["Дата", "Курс", "Изменение"])
            self.data = pd.concat([self.data, temp_df], axis=1)

        self.data["Разница"] = self.calculate_eur_usd_diff()
        self.change_types()

    def change_types(self) -> None:
        """Change type to manipulate more effective.
        Object type changes into float and datetime64"""

        self.data['Курс'] = self.data['Курс'].astype(float)
        self.data['Изменение'] = self.data['Изменение'].astype(float)
        self.data['Дата'] = self.data['Дата'].astype('datetime64')

    def calculate_eur_usd_diff(self) -> list:
        """This method calculates differ between eur and usd this way eur/usd"""

        usd = pd.to_numeric(self.data.iloc[:, 1].to_list())
        eur = pd.to_numeric(self.data.iloc[:, 4].to_list())
        return [eur[i] / usd[i] for i in range(len(eur))]

    def save_excel(self, path: str = 'currency.xlsx') -> None:
        """Save DF into file

        Parameters
        ---------------
        path: str (default current directory)"""

        self.data.to_excel(path, index=False)

    def get_data(self) -> pd.DataFrame:
        """Get dataFrame"""

        return self.data


class HandlerWebPage:
    """This class gets html page and handlers it"""

    def __init__(self):
        self.currency_url = ('https://yandex.ru/news/quotes/1.html', 'https://yandex.ru/news/quotes/23.html')
        self.data = pd.DataFrame()

    @staticmethod
    def request_data(url: str) -> str:
        """make request to get text html"""

        response = requests.get(url)
        if response.status_code != 200:
            raise ConnectionError
        return response.text

    def handle_data(self, currency: str) -> list:
        """handle html page"""

        soup = BeautifulSoup(self.request_data(currency), 'lxml')
        data_table = soup.find('table')

        result = []
        for line in data_table.find_all('tr'):
            temp = [str(item.get_text()).replace(',', '.') for item in line.find_all('td')]
            if temp:
                result.append(temp)
        return result

    def get_data(self) -> list:
        """Return list of data"""

        return [self.handle_data(currency) for currency in self.currency_url]


if __name__ == '__main__':

    web_page = HandlerWebPage()
    result = web_page.get_data()
    handler_data = HandlerDataFrame(result)
    handler_data.handle_data()
    handler_data.save_excel()

    email = EmailSender(sender_name="dim.trif1234",
                        email_name='yandex.ru',
                        sender_password="8905Lbvf1924939",
                        recipients_email=["dim.trif1234@gmail.com"], )
    email.send(subject='Currency', file='currency.xlsx')

