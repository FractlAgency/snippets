import twint

u = "USERNAME_HERE"

c = twint.Config()
c.Username = u
c.Store_csv = True
c.Output = u+".csv"
Hide_output = True
Stats = True

twint.run.Search(c)
