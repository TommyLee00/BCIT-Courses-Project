# This program produces a simulation of samples and its F value is compared with the theoretical one to test the equality of the population means
# F distribution
pop = rnorm(20000, mean=0,sd=1)
n1 = 40; n2 = 30; n3=50; n4=35
k=4
ntot = n1+n2+n3+n4
alpha= 0.10
f = c()
for(i in 1:1000){
  sample1 = sample(pop,n1)
  xb1 = mean(sample1); v1 = var(sample1)
  sample2 = sample(pop,n2)
  xb2 = mean(sample2);v2 = var(sample2)
  sample3 = sample(pop,n3)
  xb3 = mean(sample3);v3 = var(sample3)
  sample4 = sample(pop,n4)
  xb4 = mean(sample4);v4 = var(sample4)
  xb = c(xb1,xb2,xb3,xb4)
  xbb = mean(c(sample1,sample2,sample3,sample4))
  denominator = ((n1-1)*v1+(n2-1)*v2+(n3-1)*v3+(n4-1)*v4)/(ntot-k)
  numerator = sum(c(n1,n2,n3,n4)*(xb-xbb)^2)/(k-1)
  f=append(f,numerator/denominator)
}
#Plot density function
hist(f,breaks=100,freq=FALSE)
xf=seq(0,10,len=100)
lines(xf,df(xf,df1=k-1,df2=ntot-k))
#Compute critical F value
f.sorted=sort(f)
cat("Critical F value for alpha = ", alpha)
cat("Simulation: ", f.sorted[round((1-alpha)*length(f))])
cat("Theoretical: ", qf(1-alpha,df1=k-1,df2=ntot-k))


