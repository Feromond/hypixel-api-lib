class ClassExperience:
    """
    Represents a specific dungeon class experience.

    Attributes:
        experience (float): The collected experience for a given class
    """
    def __init__(self, data: dict[str,float]) -> None:
        self.experience: float = data.get("experience", 0.0)
    
    def __str__(self) -> str:
        return f"Experience: {self.experience}"

class PlayerClasses:
    """
    All dungeons player classes

    Attributes:
        healer (ClassExperience): The healer class
        mage (ClassExperience): The mage class
        berserk (ClassExperience): The berserk class
        archer (ClassExperience): The archer class
        tank (ClassExperience): The tank class
    """

    def __init__(self, data: dict[str,dict]) -> None:
        self.healer: ClassExperience = ClassExperience(data.get("healer", {}))
        self.mage: ClassExperience = ClassExperience(data.get("mage", {}))
        self.berserk: ClassExperience = ClassExperience(data.get("berserk", {}))
        self.archer: ClassExperience = ClassExperience(data.get("archer", {}))
        self.tank: ClassExperience = ClassExperience(data.get("tank", {}))

    def __str__(self) -> str:
        return f"Healer {self.healer}, Mage {self.mage}, Berserk {self.berserk}, Archer {self.archer}, Tank {self.tank}"
        
        
        