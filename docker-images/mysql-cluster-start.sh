 
echo "-------mysql cluster start------"

echo "--------start etcd --------------"
etcd -proxy on \
-listen-client-urls http://127.0.0.1:2379 \
-initial-cluster etcd0=http://etcd0:2380,etcd1=http://etcd1:2380,etcd2=http://etcd2:2380 &



/**get config**/

echo "--------start mysqld-------------"
mysqld &

