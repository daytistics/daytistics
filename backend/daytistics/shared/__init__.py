import aioinject

from .services import CryptoService, MailService

providers = [aioinject.Singleton(CryptoService), aioinject.Singleton(MailService)]
