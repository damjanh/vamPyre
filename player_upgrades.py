from enum import Enum


class PlayerUpgrades:
    def __init__(self):
        self.player_upgrades_per_level_dict = {
            1: [
                PlayerUpgrade(PlayerUpgradeType.HEALTH, 30),
                PlayerUpgrade(PlayerUpgradeType.ATTACK_DMG, 10),
                PlayerUpgrade(PlayerUpgradeType.SPEED, 0.5)
            ],
            2: [
                PlayerUpgrade(PlayerUpgradeType.HEALTH, 30),
                PlayerUpgrade(PlayerUpgradeType.ATTACK_DMG, 10),
                PlayerUpgrade(PlayerUpgradeType.SPEED, 0.5)
            ],
        }


class PlayerUpgradeType(Enum):
    HEALTH = 0,
    ATTACK_DMG = 1,
    ATTACK_SPD = 2
    SPEED = 3


class PlayerUpgrade:
    def __init__(self, upgrade_type: PlayerUpgradeType, amount):
        self.type = upgrade_type
        self.amount = amount
