 function_test_fork(){
	sleep 10000;
	echo "this is test fork";

}

echo "first"
function_test_fork &
echo "end"