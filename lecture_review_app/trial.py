import databaseconnection
engine = databaseconnection.initialize()
# databaseconnection.enter(engine)
# print databaseconnection.login(engine,"shruti.p@gmail.com","pwd")
databaseconnection.print_lec_ids(engine)
