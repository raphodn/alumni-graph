'use strict';

dbapp.factory('dbFactory', ['$http', function($http) {
        
	var dbFactory = {};



	var apiUrlBase = '/api/';


	dbFactory.getAllData = function () {
    	return $http({
	      	url: apiUrlBase,
	      	method: 'GET'
    	});
	};

	dbFactory.postDatabase = function(db_file) {

	   	return $http({
			url: apiUrlBase,
			method: 'POST',
			headers: {'Content-Type': undefined},
			transformRequest: function (data) {
				var fd = new FormData();
				fd.append("db", db_file);
   				return fd;
   			}
   		});
	};




    return dbFactory;

}]);//end of dbFactory