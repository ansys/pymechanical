from ansys.mechanical.core import App

app = App(version=251)
app.open(r"D:\PyAnsys\Repos\exp\pymechanical\tests\assets\cube-hole.mechdb")
app.message
app.message.print()
app.message.add("info", "User clicked the start button.")
app.message.print(complete_info=True)

# app.message.print()  # Combines messages from ExtAPI and local messages
# app.message.add("DEBUG", "User clicked the start button.")
# app.message.print()  # Combines messages from ExtAPI and local messages

# app.message.clear_local_messages()
# app.message.print()  # Only messages
