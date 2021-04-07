# This program creates a simulation of a sample and its confidence interval of population mean and standard deviation are compared with the theoretical values
# Confidence interval for population mean
xb0 =21.3
s0 = 0.7
n=4
alpha = 0.05
ns = 1000
population = rnorm(3000,mean=xb0,sd=s0)
hist(population,breaks= 30)
     
xbar = rep(0,ns)
for(i in 1:ns) xbar[i] = mean(sample(population,n))
hist(xbar,breaks=30)

left = round(ns*alpha/2); right = round(ns*(1-alpha/2))
xbar.sorted = sort(xbar,method="quick")
cat("Simulation: ", xbar.sorted[left]," < mu < ", xbar.sorted[right])

#Theoretical result for comparison
E = qnorm(1-alpha/2)*s0/sqrt(n)
cat("Theoretical: ", xb0-E, " < mu < ", xb0+E)

# Confidence interval for population sd
xb0 =21.3
s0 = 0.7
n=4
df=n-1
alpha = 0.05
ns = 1000
population = rnorm(3000,mean=xb0,sd=s0)
hist(population,breaks= 30)

s = rep(0,ns)
for(i in 1:ns) s[i] = sd(sample(population,n))
hist(((n-1)*(s^2))/(s0^2),breaks=30)
left = round(ns*(alpha/2)); right = round(ns*(1-alpha/2))
s.sorted = sort(s,method="quick")
chisqleft = s0^2/(s.sorted[left])
chisqright = s0^2/(s.sorted[right])
cat("Simulation: ", chisqright," < sigma < ", chisqleft)

#Theoretical result for comparision
theochisqleft = qchisq(alpha/2,df)
theochisqright = qchisq(1-alpha/2,df)
theosigmaleft = s0*sqrt((n-1)/theochisqleft)
theosigmaright = s0*sqrt((n-1)/theochisqright)
cat("Theoretical: ", theosigmaright, " < sigma < ", theosigmaleft)

