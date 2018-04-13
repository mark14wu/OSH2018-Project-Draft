import sys
filename = sys.argv[1]
content = open(filename).read()
content_list = content.split('\n')
new_list = []
for x in content_list:
    if x is not '':
        new_list.append(x)
print(new_list)
content = '\n\n'.join(new_list)
open('test.md', 'w').write(content)