# 🍽️ main.py
# A simple FastAPI project that demonstrates Dependency Injection through a Royal Kitchen story

from fastapi import FastAPI, Depends

app = FastAPI()


# 🔧 STEP 1: Define Ingredients (These are the "Dependencies")
# These are things that other parts of your app might need.
# Think of them as tools or services you can inject into classes or functions.

# TomatoSauce is an ingredient used by ItalianChef
class TomatoSauce:
    def flavor(self):
        return "Tangy and fresh tomato sauce"


# MasalaMix is an ingredient used by IndianChef
class MasalaMix:
    def flavor(self):
        return "Spicy and aromatic Indian masala"


# 👨‍🍳 STEP 2: Define Chefs (These are the "Services" that depend on ingredients)
# These chefs require specific ingredients to cook their dishes.
# But they don't create those ingredients themselves — they receive them from outside.

class ItalianChef:
    # Constructor injection: Chef receives dependency (TomatoSauce) externally
    def __init__(self, sauce: TomatoSauce):  # <-- DEPENDENCY INJECTION POINT
        self.sauce = sauce

    def cook(self):
        return f"Italian Pasta with {self.sauce.flavor()}"


class IndianChef:
    # Constructor injection: Chef receives dependency (MasalaMix) externally
    def __init__(self, masala: MasalaMix):  # <-- DEPENDENCY INJECTION POINT
        self.masala = masala

    def cook(self):
        return f"Butter Chicken with {self.masala.flavor()}"


# 📦 STEP 3: Create Dependency Provider Functions
# These functions tell FastAPI how to provide the dependencies when needed.
# This is where injection happens in FastAPI routes.

def get_tomato_sauce():
    # Returns an instance of TomatoSauce
    return TomatoSauce()


def get_masala_mix():
    # Returns an instance of MasalaMix
    return MasalaMix()


# 🚀 STEP 4: API Endpoints (Chefs enter the kitchen!)
# Here  we use Depends() to inject dependencies at runtime,
# which allows us to switch or mock dependencies easily.

@app.get("/italian-chef")
def italian_chef_dishes(sauce: TomatoSauce = Depends(get_tomato_sauce)):
    # Dependency injected via route parameter using Depends()
    # ↑↑↑ This is where Dependency Injection happens!
    chef = ItalianChef(sauce=sauce)  # Passing the injected sauce to the chef
    return {"dish": chef.cook()}


@app.get("/indian-chef")
def indian_chef_dishes(masala: MasalaMix = Depends(get_masala_mix)):
    # Dependency injected via route parameter using Depends()
    # ↑↑↑ This is where Dependency Injection happens!
    chef = IndianChef(masala=masala)  # Passing the injected masala to the chef
    return {"dish": chef.cook()}
