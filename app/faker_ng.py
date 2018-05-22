from faker import Faker
import random
fake = Faker()

from faker.providers import BaseProvider

class FakerNigeriaProvider(BaseProvider):
    first_names = ['Tola', 'Funmi', 'Ugo', 'Chima', 'Chioma', 'Bem', 'Bolu', 'Bola', 'Hassan', 'Ahmed', 'Usman', 'Abdul', 'Hawa', 'Bisi', 'Abiodun', 'Collins', 'Bassey', 'Stella', 'Chichi', 'Kola', 'Gboyega', 'Niyi', 'Deolu', 'Deola', 'Kelvin', 'Mika', 'Jaden', 'Jennifer', 'Tope', 'Wale', 'Shehu', 'Dino', 'Abang', 'Ijeoma', 'Victor', 'Paul', 'Idowu', 'Kome', 'Onome', 'Nkechi', 'Tochi', 'Fola', 'Tunde']

    last_names = ['Awoyi', 'Amosun', 'Abatan', 'Chidera', 'Agu', 'Agumanu', 'Ejiofor', 'Kabir', 'Nenge', 'Odusanya', 'Popoola', 'Tersoo', 'Aduba', 'Adoti', 'Baba', 'Agrinya', 'Bolaji', 'Iwuchukwu', 'Okoye', 'Obasanjo', 'Akintola', 'Tinubu', 'Dimka', 'Ibori', 'Odili', 'Jalloh', 'Mensah', 'Akiloye', 'Sekibo', 'Akpabio', 'Effiong', 'Osei', 'Osian', 'Olarewaju', 'Oyinlola', 'Igwe', 'Sane', 'Jakande', 'Obi', 'Uba', 'Falana', 'Okiro', 'Onobanjo', 'Aguda']

    def first_name(self):
        return random.choice(self.first_names)

    def last_name(self):
        return random.choice(self.last_names)

    def name(self):
        return "{} {}".format(random.choice(self.first_name), random.choice(self.last_name))


fake.add_provider(FakerNigeriaProvider)
