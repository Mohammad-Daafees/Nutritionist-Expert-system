from experta import *
from experta.fact import *
class action (Fact):
    pass
class status (Fact):
    pass
def calculate_bmr(gender, age, weight, height):
    """
    Calculate BMR using the Mifflin-St Jeor Equation.
    gender: 'male' or 'female'
    age: in years
    weight: in kilograms
    height: in centimeters
    """
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender.lower() == 'female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Gender must be 'male' or 'female'")
    
    return bmr

def calculate_calories(bmr, activity_level):
    """
    Calculate daily calorie needs based on activity level.
    activity_level: a string representing the level of physical activity
    """
    activity_multipliers = {
        'sedentary': 1.2,          # Little or no exercise
        'lightly active': 1.375,   # Light exercise/sports 1-3 days/week
        'moderately active': 1.55, # Moderate exercise/sports 3-5 days/week
        'very active': 1.725,      # Hard exercise/sports 6-7 days a week
        'extra active': 1.9        # Very hard exercise/physical job & exercise twice a day
    }

    if activity_level.lower() not in activity_multipliers:
        raise ValueError("Invalid activity level. Choose from: 'sedentary', 'lightly active', 'moderately active', 'very active', 'extra active'")
    
    return bmr * activity_multipliers[activity_level.lower()]
    
    return bmr * activity_multipliers.get(activity_level.lower(), 1.2)  # Default to sedentary if not found
instruction=[];
# Low sodium foods that are not high in calories
# Shortened lists

# Low sodium, low calories
low_sodium_low_calories = [
    "Cucumbers",
    "Spinach",
    "Broccoli"
]

# Low sugar foods that are not high in calories
low_sugar_low_calories = [
    "Avocado",
    "Plain Greek Yogurt",
    "Chicken Breast"
]

# Low sodium foods that are high in calories
low_sodium_high_calories = [
    "Almonds",
    "Peanut Butter",
    "Olive Oil"
]

# Low sugar foods that are high in calories
low_sugar_high_calories = [
    "Nuts (like walnuts, pecans)",
    "Full-Fat Dairy Products (like whole milk, cream)",
    "Fatty Fish (like mackerel)"
]

# High sodium foods
high_sodium_foods = [
    "Soy Sauce",
    "Pickles",
    "Bacon"
]

# High sugar foods
high_sugar_foods = [
    "Candy (like gummy bears, chocolate bars)",
    "Soda and Soft Drinks",
    "Ice Cream"
]

Weight=0
Height=0.0
age=0
gender=" "
class Person(Fact):
    gender = Field(str, mandatory=True)
    age = Field(int, mandatory=True)
    Weight = Field(int, mandatory=True)
    Height=Field(float,mandatory=True)
    



class nutritionist (KnowledgeEngine):
    
 
       
    
    @Rule()
    def startup(self):
        Weightt = int(input("Enter Your Weight In KG: "))
        Heightt = float(input("Enter Your Height In Meters: "))
        agee=int(input("enter your age"))
        genderr=str(input("are you a male or female?"))
        self.declare(Person(gender=genderr,age=agee,Weight=Weightt,Height=Heightt*100))
        BMI = Weightt / (Heightt * Heightt)
        self.declare(Fact(BmiValue=BMI))
        print(f"Your BMI is {BMI:.2f}")
        if BMI <= 18.4:
            self.declare(Fact(BMIstatus="underweight"))
            instruction.append(" You need to gain Weight")
            self.declare(status(AbnormalBMI='Y'))
        elif 18.5 <= BMI < 24.9:
            self.declare(Fact(BMIstatus="normal"))
            print("you are fine thx for visiting")
            self.declare(status(AbnormalBMI='N'))
        elif 25 <= BMI < 29.9:
            self.declare(Fact(BMIstatus="overweight"))
            self.declare(status(AbnormalBMI='Y'))
            instruction.append(" You need to lose Weight")
        else:
            self.declare(Fact(BMIstatus="obese"))
            self.declare(status(AbnormalBMI='Y'))
            instruction.append(" You need to Lose a lot of Weight")
       

    @Rule(status(AbnormalBMI='Y'))
    def abnormalBMI(self):
        musclesChoice=input(" Do you wanna Build muscles ?")
        print("choice is : ", musclesChoice)
        if(musclesChoice=='Y'):
            instruction.append("You should take Higher Protein") 
        self.declare(action("Medical-Condition"))
    @Rule(action("Medical-Condition"))
    def MedicalCondition(self):
        if (input("do you have Diabetic?")=='Y' ):
            self.declare(status('Diabetic'))
            instruction.append("You should have a low sugar diet with controlled carb consumption and avoid these foods: %s" % ', '.join(high_sugar_foods))

        if (input("do you have hypertensive?")=='Y' ):
            self.declare(status('hypertensive'))
            instruction.append("You should have a low sodium diet and avoid these foods: %s" % ', '.join(high_sodium_foods))
        self.declare(action("activity-level"))
    @Rule(action("activity-level"))
    def activityLevel(self):

        activityLevel=input("How active are you? \n sedentary:   Little or no exercise \n lightly active:   Light exercise/sports 1-3 days/week  \n moderately active:   Moderate exercise/sports 3-5 days/week \n very active: Hard exercise/sports 6-7 days a week\n extra active:Very hard exercise/physical job & exercise twice a day")
        self.declare(Fact(activity=activityLevel))
        self.declare(action('Dietary-Habits'))


    @Rule(action("Dietary-Habits"))
    def DietaryHabits(self):
        if(input("do you consume High amount of processed Food?")=="Y"):
            instruction.append("you should eat less processed food")
        if(input("do you consume enough amount of fruites and vegetables?")=="N"):
            instruction.append("you should eat more fruites and vegetables")
        if(input("do you consume enough amount of water?")=="N"):
            instruction.append("you should drink more water")
        self.declare(action("Food-Restrictions"))
    @Rule(action("Food-Restrictions"))
    def FoodRestrictions(self):
        if (input("Do you have any food restrictions?")=="Y"):
            x=" "
            while (x != "exit"):
                x=input(
                "Enter the name of food you don't want in your diet enter exit when done"
                )
                if x in low_sodium_low_calories:
                    low_sodium_low_calories.remove(x)
                if x in low_sodium_high_calories:
                    low_sodium_high_calories.remove(x)
                if x in low_sugar_high_calories:
                    low_sugar_high_calories.remove(x)
                if x in low_sugar_low_calories:
                    low_sugar_low_calories.remove(x)
        self.declare(action("final-phase"))
    @Rule(action("final-phase"))
    def finalFunction(self):
        person_fact = self.facts[1]
        bmr=calculate_bmr(weight=person_fact['Weight'],height=person_fact['Height'],age=person_fact['age'],gender=person_fact['gender'])
        activityLev=" "
        for fact in self.facts.values():
            if 'activity' in fact:
                
                activityLev= fact
        calories=calculate_calories(bmr,activity_level=activityLev['activity'])
        instruction.append(f"Your base daily calories to maintain weight is {calories}. For healthy weight loss, subtract 500 calories, and for healthy weight gain, add 500 calories.") 
        self.declare(action("Recommend-Food"))
        

    
    @Rule(AND(status("Diabetic"), Fact(BMIstatus='underweight'), action("Recommend-Food")))
    def diabetic_underweight(self):
       instruction.append("You should have a low sugar diet but high calories i recommend these foods: %s" % ', '.join(low_sugar_high_calories))

    @Rule(AND(status("Diabetic"), Fact(BMIstatus=MATCH.BMIstatus), 
              status(AbnormalBMI='Y'), TEST(lambda BMIstatus: BMIstatus in ['overweight', 'obese']), 
              action("Recommend-Food")))
    def diabetic_overweight_or_obese(self, BMIstatus):
        instruction.append("You should have a low sugar diet and low calories i recommend these foods: %s" % ', '.join(low_sugar_low_calories))
        

    @Rule(AND(status("Hypertensive"), Fact(BMIstatus='underweight'), action("Recommend-Food")))
    def hypertensive_underweight(self):
         instruction.append("You should have a low sodium diet and high calories i recommend these foods: %s" % ', '.join(low_sodium_high_calories))
        

    @Rule(AND(status("Hypertensive"), Fact(BMIstatus=MATCH.BMIstatus), 
              status(AbnormalBMI='Y'), TEST(lambda BMIstatus: BMIstatus in ['overweight', 'obese']), 
              action("Recommend-Food")))
    def hypertensive_overweight_or_obese(self, BMIstatus):
       instruction.append("You should have a low sodium diet and low calories i recommend these foods: %s" % ', '.join(low_sodium_low_calories))
       
        

        

   
                

        
        

        





eng=nutritionist()
eng.reset()
eng.run()
print(instruction)

