import re

def objOne(fileContent: str):
    rules = re.split("\n", re.split("\n\n", fileContent, 1)[0])
    orders = re.split("\n", re.split("\n\n", fileContent, 1)[1])

    rulesDict = {}
    for rule in rules:
        key = int(re.split("\|", rule, 1)[0])
        value = int(re.split("\|", rule, 1)[1])
        # Each entry of rulesDict will have an array for each key
        if key in rulesDict.keys():
            rulesDict[key].append(value)
        else:
            rulesDict[key] = [value]
    correctOrders = 0
    for order in orders:
        orderArray = list(map(int, re.split(",", order)))
        correctOrders += checkOrderAgainstRulesPt1(orderArray, rulesDict)
    print(correctOrders)

def checkOrderAgainstRulesPt1(orderArr: list, rules: dict) -> int:
    printedPages = []
    for page in orderArr:
        if (page in rules.keys()):
            # Rule found for current page, check then add if ok
            for prevPage in printedPages:
                # One of the previous pages broke the rule!!!
                if prevPage in rules[page]:
                    return 0
            printedPages.append(page) # Didn't break the rule, add
        else:
            # No rule for current page
            printedPages.append(page)
    return printedPages[int(len(printedPages)/2)]

def objTwo(fileContent: str):
    rules = re.split("\n", re.split("\n\n", fileContent, 1)[0])
    orders = re.split("\n", re.split("\n\n", fileContent, 1)[1])

    rulesDict = {}
    for rule in rules:
        key = int(re.split("\|", rule, 1)[0])
        value = int(re.split("\|", rule, 1)[1])
        # Each entry of rulesDict will have an array for each key
        if key in rulesDict.keys():
            rulesDict[key].append(value)
        else:
            rulesDict[key] = [value]
    incorrectOrderSum = 0
    for order in orders:
        orderArray = list(map(int, re.split(",", order)))
        incorrectOrderSum += checkOrderAgainstRulesPt2(orderArray, rulesDict)
    print(incorrectOrderSum)

def checkOrderAgainstRulesPt2(orderArr: list, rules: dict) -> int:

    incorrectOrder = checkOrderAgainstRulesPt1(orderArr, rules) == 0
    if not incorrectOrder:
        return 0
    
    count = 0
    #print("Beginning order is " + str(orderArr))
    # Ok we are gonna try to do a modified insertion sort on this one
    # Go through each page, and check each already currently inserted 
    insertionSortedArray = []
    for page in orderArr:
        location = 0 # Index to insert it 
        for otherPageIndex in range(len(insertionSortedArray)): # for every page already sorted
            #if page == 47:
                #print("Testing 47 against " + str(insertionSortedArray[otherPageIndex]))
                #print("47 would output a " + str(insertionSortedArray[otherPageIndex] in rules.keys()) + " " + (str(page in rules[insertionSortedArray[otherPageIndex]]) if insertionSortedArray[otherPageIndex] in rules.keys() else "False") + " on the first if statement")
                #print("47 would output a " + str((page in rules.keys())) + " " + (str(insertionSortedArray[otherPageIndex] in rules[page]) if str((page in rules.keys())) else "False") + " on the second if statement")

            if (insertionSortedArray[otherPageIndex] in rules.keys()) and (page in rules[insertionSortedArray[otherPageIndex]]): # check if the page to be inserted is in this already sorted page's rules (meaning this page should come after it)
                if location < len(insertionSortedArray): # Page must come after insertionSortedArray[otherPageIndex]
                    location = otherPageIndex + 1
            if (page in rules.keys()) and (insertionSortedArray[otherPageIndex] in rules[page]):
                # Page must come before this element
                if location != 0 and otherPageIndex < location: # Dunno why this otherPageIndex < location works :/ my brain is fried tonight
                    location = otherPageIndex # Since it moves forward otherPage
        #if page == 47:
            #print("47 will be inserted at " + str(location))
        insertionSortedArray.insert(location, page)
        # Check if insertionSortedArray is sorted (should be, just a sanity check)
        #if (len(insertionSortedArray) != 0):
            #print("List is sorted?: " + str(checkOrderAgainstRulesPt1(insertionSortedArray, rules)) + "; List is " + str(insertionSortedArray))
    #print("Final sorted array is " + str(insertionSortedArray))

    #while incorrectOrder and count < 10:
    #   printedPages = []
    #    count += 1
    #    print("Not in correct order, array is " + str(orderArr))
    #    incorrectOrder = checkOrderAgainstRulesPt1(orderArr, rules) == 0


    return insertionSortedArray[int(len(insertionSortedArray)/2)]

if __name__ == "__main__":
    with open("advent_of_code_2024\\andrew\\Day5.txt") as file:
        objTwo(file.read())

# If rule is 1|2 and array = [2, 3, 2, 1], 1 must be before 2
# if you swap 1 with the first out of order element, array becomes [1, 3, ]