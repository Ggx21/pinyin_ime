class check_answer():
    # check the correctness of the answer, and calculate the accuracy of single character and whole sentence

    def __init__(self,answer_file,correct_answer_file):
        self.std_output=[]
        self.my_output=[]
        self.answerlength=0
        self.total_characters=0

        with open(answer_file,"r",encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                self.my_output.append(line)
        with open(correct_answer_file,"r",encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                self.std_output.append(line)
        self.answerlength=len(self.std_output)

    def get_total_characters(self):
        for i in range(self.answerlength):
            self.total_characters+=len(self.std_output[i])
        return self.total_characters

    def check_sentence(self):
        # check the correctness of the whole sentence
        correct=0
        for i in range(self.answerlength):
            if self.std_output[i]==self.my_output[i]:
                correct+=1
        accu=correct/self.answerlength
        # covert to percentage, and round to 2 decimal places
        accu=round(accu*100,2)
        return  str(accu)+"%"

    def check_character(self):
        # check the correctness of single character
        correct=0
        for i in range(self.answerlength):
            for j in range(len(self.std_output[i])):
                if self.std_output[i][j]==self.my_output[i][j]:
                    correct+=1
        accu=correct/self.get_total_characters()
        # covert to percentage, and round to 2 decimal places
        accu=round(accu*100,2)
        return str(accu)+"%"

    def run(self):
        print("running...")
        print("checking the answer...")
        print("the accuracy of the whole sentence is: ",self.check_sentence())
        print("the accuracy of single character is: ",self.check_character())

if __name__ == "__main__":
    check=check_answer("output.txt","std_output.txt")
    check.run()