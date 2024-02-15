from app.lib.models.config import ConfigModel
from app import db


class SettingsManager:
    def __init__(self) -> None:
        self.insert_if_not_exists('hashcat_binary', '/usr/local/bin/hashcat')
        self.insert_if_not_exists('hashcat_status_interval', 10)
        self.insert_if_not_exists('hashcat_force', 0)

        self.insert_if_not_exists('wordlists_path', '/opt/wordlists')
        self.insert_if_not_exists('hashcat_rules_path', '/opt/rules')
        self.insert_if_not_exists('hashcat_masks_path', '/opt')
        
        self.insert_if_not_exists('uploaded_hashes_path', '/tmp')

    def insert_if_not_exists(self, name, value):
        setting = ConfigModel.query.filter(ConfigModel.name == name).first()
        if setting is None:
            setting = ConfigModel(name=name, value=value)
            db.session.add(setting)

            db.session.commit()
            return True
        return False

    def save(self, name, value):
        setting = ConfigModel.query.filter(ConfigModel.name == name).first()
        if setting is None:
            setting = ConfigModel(name=name, value=value)
            db.session.add(setting)
        else:
            setting.value = value

        db.session.commit()

        return True

    def get(self, name, default=None):
        setting = ConfigModel.query.filter(ConfigModel.name == name).first()
        if setting is None:
            return default
        return setting.value
