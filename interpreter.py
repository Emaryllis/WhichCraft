def interpret_whichcraft(code):
    code_lines = code.split('\n')
    tabs = ''
    newCode = ''
    for line in code_lines:
        newCode += '\n'+tabs
        line = line.replace('CONJURED WITH', '+').replace('NOT DESTINED AS', '!=').replace('DESTINED AS', '==').replace('EVANESCED WITH', '-').replace('REPLICATED WITH', '*').replace(
            'DISSEVERANCED WITH', '/').replace('INFERIOR TO', '<').replace('SUPERIOR TO', '>').replace('AN EMPTY BAG', '[]')
        if line.startswith('NEW INCANTATION'):
            data = line.replace('NEW INCANTATION ', '').split(' ')
            newCode += f'def {data[0]}({", ".join(data[1:])}):'
            tabs += ' '*4
        elif (
            line.startswith('ALIGNMENT CEASURE')
            or line.startswith('INCANTATION CLOSURE')
            or line.startswith('SPELL CONCLUSION')
        ):
            tabs = tabs[:-4]
        elif line.startswith('SUMMON'):
            variable = line.replace('SUMMON ', '')
            if ' ' in variable:
                raise SyntaxError(f'Invalid variable declaration ({line})')
            newCode += f'{variable} = None'
        elif line.startswith('WHEN THE STARS ALIGN'):
            newCode += f'if{line.replace("WHEN THE STARS ALIGN","")}:'
            tabs += ' '*4
        elif line.startswith('TRANSMUTE'):
            line = line.replace('TO', '=').replace('TRANSMUTE ', '')
            index = line.find('=')
            if line[index+2:].startswith('INCANTATION'):
                newCode += line[:index+1]
                data = line[index+2:].replace('INCANTATION ', '').split(' ')
                newCode += f' {data[0]}({", ".join(data[1:])})'
            else:
                newCode += line
        elif line.startswith('ALTERNATIVELY'):
            newCode = f'{newCode[:-4]}else:'
        elif line.startswith('UNLEASH THE HEX OF'):
            errorType = line.replace('UNLEASH THE HEX OF ', '').split(' ')[0]
            newCode += f'raise {errorType}({line.replace("UNLEASH THE HEX OF ", "").replace(f"{errorType} ", "")})'
        elif line.startswith('UNVEIL'):
            newCode += f'return {line.replace("UNVEIL ", "")}'
        elif line.startswith('REPEAT SPELL'):
            newCode += f'while {line.replace("REPEAT SPELL ", "").replace("WHEN ","")}:'
            tabs += ' '*4
        elif line.startswith('CAST UP'):
            data = line.replace('CAST UP ', '').split(' ')
            if len(data) > 3:
                raise SyntaxError(f'Invalid list appending ({line})')
            newCode += f'{data[2]}.append({data[0]})'
        elif line.startswith('SCROLL REVELATION'):
            newCode += f'print({line.replace("SCROLL REVELATION ", "")})'
        elif line.startswith('INCANTATION'):
            data = line.replace('INCANTATION ', '').split(' ')
            newCode += f'{data[0]}({", ".join(data[1:])})'
    if tabs != '':
        raise SyntaxError('Invalid indentation, please check your code.')
    return newCode


if __name__ == '__main__':
    fileName = input('Enter the relative path file name to interpret: ')

    if '.wc' not in fileName:
        fileName += '.wc'
    try:
        with open(fileName, 'r') as file:
            exec(interpret_whichcraft(file.read()))
    except FileNotFoundError:
        print(f'File {fileName} was not found.')

# NEW INCANTATION enchanting_calculator operation num1 num2
# NEW INCANTATION castSpell operation num1 num2
# SUMMON potion_result
# WHEN THE STARS ALIGN operation DESTINED AS 'add'
# TRANSMUTE potion_result TO num1 CONJURED WITH num2
# ALIGNMENT CEASURE
# WHEN THE STARS ALIGN operation DESTINED AS 'subtract'
# TRANSMUTE potion_result TO num1 EVANESCED WITH num2
# ALIGNMENT CEASURE
# WHEN THE STARS ALIGN operation DESTINED AS 'multiply'
# TRANSMUTE potion_result TO num1 REPLICATED WITH num2
# ALIGNMENT CEASURE
# WHEN THE STARS ALIGN operation DESTINED AS 'divide'
# WHEN THE STARS ALIGN num2 NOT DESTINED AS 0
# TRANSMUTE potion_result TO num1 DISSEVERANCED WITH num2
# ALTERNATIVELY
# UNLEASH THE HEX OF ValueError 'Error: Cannot divide by zero!'
# ALIGNMENT CEASURE
# ALIGNMENT CEASURE
# UNVEIL potion_result
# INCANTATION CLOSURE
# SUMMON result_list
# TRANSMUTE result_list TO AN EMPTY BAG
# REPEAT SPELL WHEN count INFERIOR TO 4
# TRANSMUTE potion_result TO INCANTATION cast_spell operation num1 num2
# CAST UP potion_result INTO result_list
# TRANSMUTE count TO count CONJURED WITH 1
# SPELL CONCLUSION
# SCROLL REVELATION 'The result is: ' CONJURED WITH result_list
# INCANTATION CLOSURE
# INCANTATION enchanting_calculator 'add' 5 3
# INCANTATION enchanting_calculator 'subtract' 10 2
# INCANTATION enchanting_calculator 'multiply' 4 6
# INCANTATION enchanting_calculator 'divide' 15 3
