from django import template

register = template.Library()

@register.simple_tag
def calculation_marks( value ):
    try:
        value = int(value)

        if value>=90 and value<=100:
            return('A+')
        elif value>=80 and value<=90:
            return('A')
        elif value>=70 and value<=80:
            return('B+')
        elif value>=60 and value<=70:
            return('B')
        elif value >=50 and value<=60:
            return('C+')
        elif value>=40 and value<=50:
            return('C')
        else:
            return('Fail')
            
    except:
        pass
    return ''