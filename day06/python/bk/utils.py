def groupeData(data):
    result=[]
    groupedData=[]
    added=False
    for d in data:
        if not d.strip():
            result.append(groupedData)
            groupedData=[]
            added=True
        else:
            d=removeLineBreaks(d)
            groupedData.append(d)
            added=False
    if added == False:
        result.append(groupedData)
    return result
def removeLineBreaks(value):
    value = value.replace("\r","")
    value = value.replace("\n","")
    return value
