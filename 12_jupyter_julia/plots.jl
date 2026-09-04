using Plots
plotly()

x = range(0, 10, length=100)
y = sin.(x)
p = plot(x, y)
display(p)
println("Press enter key to quit:")
readline()
