def inp_range(a,b):
    isInt = lambda x:x.isnumeric()
    inRange = lambda x:a<=int(x)<b
    return ( (isInt, "Du måste ange ett heltal. Försök igen."),\
    (inRange,"Du måste ange ett tal mellan {0} och {1}. Inklusive {0} men ej {1}. Försök igen.".format(a,b)) )
def inp_opts(opts):
    isOption = lambda x:x in opts
    return ((isOption, "Det var inte ett alternativ. Ange något av"+opts.__str__()[1:-1]),)
    

def get_inp(conds, txt1, end="\n", conv=lambda x:x):
        """Keeps asking the user for input untill given a value that fulfills all conds.
         Takes an ordered iterable object of pairs with conditions and corresponding error messages that are complemented with end.
         Each condition function has to be capable of taking arbitrary string inputs that has passed all previous conditions."""
        ask_str = txt1
        while True:
            res = input(ask_str+end)
            is_legit = True
            for cond, err in conds:
                if not cond(res):
                    is_legit = False
                    ask_str = err
                    break
            if is_legit:
                break
        return conv(res)

if __name__ == "__main__":
    inp = 10
    while inp:
        inp = get_inp(inp_opts(("apa","banan","tryffel")), "Ange ett alternativ", end="\t", conv = lambda x:2*x)
        print("Du lyckades "+inp)
        inp = get_inp(inp_range(1,11), "Ange ett heltal.", conv = int)
        print("Du lyckades "+str(inp))