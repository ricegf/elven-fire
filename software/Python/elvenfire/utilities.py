
def wrapped(text, length=76, indent=0):

    lines = text.split('\n')
    wrapped = []

    while lines:
        line = lines.pop(0)
        while len(line) > length:
            i = line.rfind(' ', 0, length)
            if i < indent:
                wrapped.append(line[:length-1] + '-')
                line = ' ' * indent + line[length-1:]
            else:
                wrapped.append(line[:i])
                line = ' ' * indent + line[i+1:]
        wrapped.append(line)

    return '\n'.join(wrapped)
        