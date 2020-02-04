import os
import sys
import datetime

learningRate = [0.010]#[0.002, 0.010]
TrainingEpoch = [5]#[10, 20]
BatchSize = [40]#30
numberExecutor = [1]#1

# previous Home Folder
f=open('homename.txt')
flist=f.readlines()
preHome=flist[0].split('/')[-1].strip()
print('previous HomeFolder is {}'.format(preHome))
print('-------------------------------------------')

# fetch the name of home folder 
os.system('cd ~ ; pwd > ~/Runner/homename.txt')
f=open('homename.txt')
flist=f.readlines()
HOMEFOLDER=flist[0].split('/')[-1].strip()
print('Current Homefolder is {}'.format(HOMEFOLDER))
f.close()
print('-------------------------------------------')

# adjust paths in config file 
f=open('/home/%s/Runner/config.json'%HOMEFOLDER,'r+')
flist=f.readlines()
for i in range(len(flist)):
	flist[i]=flist[i].replace(preHome, '{}'.format(HOMEFOLDER))
f=open('/home/{}/Runner/config.json'.format(HOMEFOLDER),'w+')
f.writelines(flist)
f.close()
print('Paths in config.json adjusted')
print('-------------------------------------------')

# fetch internal ip address
os.system('ip add > ipaddress.txt')
f=open('ipaddress.txt')
flist=f.readlines()
ip=flist[8].strip().split(' ')[1]
ip=ip.split('/')[0].strip()
print('Current internal IP address is {}'.format(ip))
f.close()
print('-------------------------------------------')

f=open('/home/{}/bd/spark/conf/spark-env.sh'.format(HOMEFOLDER),'r+')
flist=f.readlines()
flist[69]="SPARK_MASTER_HOST='{}'\n".format(ip)
f=open('/home/{}/bd/spark/conf/spark-env.sh'.format(HOMEFOLDER),'w+')
f.writelines(flist)
f=open('/home/%s/Runner/config.json'%HOMEFOLDER,'r+')
flist=f.readlines()
flist[31]='  "master": "spark://{}:7077",\n'.format(ip)
f=open('/home/%s/Runner/config.json'%HOMEFOLDER,'w+')
f.writelines(flist)
f.close()
print('current master ip address is set to be: {}'.format(ip))
print('-------------------------------------------')

# Only use for single node mode
# # spark set up
# os.system('/home/%s/bd/spark/sbin/stop-all.sh'%HOMEFOLDER)
# os.system('/home/%s/bd/spark/sbin/start-master.sh'%HOMEFOLDER)
# print('master node initialized')
# print('please input slave node internal ip address:')
# tmp=input()
# if len(tmp)==0:
# 	tmp=ip
# 	os.system('/home/{}/bd/spark/sbin/start-slave.sh spark://{}:7077'.format(HOMEFOLDER,tmp))
# 	print('slave {} has been connected'.format(tmp))
# 	print('-------------------------------------------')
# else:
# 	while len(tmp)!=0:
# 		os.system('/home/{}/bd/spark/sbin/start-slave.sh spark://{}:7077'.format(HOMEFOLDER,tmp))
# 		print('slave {} has been connected'.format(tmp))
# 		print('please input slave node internal ip address:')
# 		tmp=input()
# print('slave nodes initialized over')
# print('-------------------------------------------')

now = datetime.datetime.now()
experiment = now.isoformat()
count=12

#for replication in range(0, nReplications): Can already be seen as 3 replications???
for lr in learningRate:
	for epoch in TrainingEpoch:
		for executor in numberExecutor:
			for size in BatchSize:
				count+=1
				f=open('/home/%s/Runner/config.json'%HOMEFOLDER,'r+')
				flist=f.readlines()
				flist[6]='            "totalExecutorCores": "{}",\n'.format(executor)
				flist[20]='            "batchSize": "{}",\n'.format(size)
				flist[21]='            "maxEpoch": "{}",\n'.format(epoch)
				flist[22]='            "learningRate": "{}",\n'.format(lr)
				f=open('/home/%s/Runner/config.json'%HOMEFOLDER,'w+')
				f.writelines(flist)
				f.close()
				os.system('/home/%s/bd/sparkgen-bigdl/sparkgen -r -d -c /home/%s/Runner/config.json'%(HOMEFOLDER,HOMEFOLDER))
				os.system('mkdir -p /home/%s/Runner/Result/%s_lr%s_ep%s_ex%s_s%s'%(HOMEFOLDER,count,lr,epoch,executor,size))
				os.system('mv /home/%s/Runner/test/* /home/%s/Runner/Result/%s_lr%s_ep%s_ex%s_s%s'%(HOMEFOLDER,HOMEFOLDER,count,lr,epoch,executor,size))
				print('current experiment count is {}'.format(count))
				print('-------------------------------------------')
print('finished! Total experiment count is: {}'.format(count))
print('Total time cost is: {}'.format(datetime.datetime.now()-now))
print('-------------------------------------------')
