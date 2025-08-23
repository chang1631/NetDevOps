from jinja2 import Template

input_name = input("Enter your name: ")

tm = Template("Hello {{name}}")
msg = tm.render(name=input_name)

print(msg)