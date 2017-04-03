var app = angular.module('app', ['ngTagsInput', 'ngAvatar']);

app.controller('main', function ($scope, $http, $sce) {
	$scope.searchSkills = [ 'js' ];
	$scope.limit = 20;

	$scope.skillTypeAhead = function (keyword) {
		return [];
	};

	// Profile URL
	$scope.profileURL = function (name) {
		return 'https://www.linkedin.com/search/results/index/?keywords=' + name;
	}

	$scope.highlightSkill = function(text) {
		

		var skills = [];
		$scope.searchSkills.forEach(function (i) {
			skills.push(i.text)
		});
		var search = skills.join('|');
		if (!search) {
			return $sce.trustAsHtml(text);
		}
		return $sce.trustAsHtml(text.replace(new RegExp(search, 'gi'), '<span class="highlightedText">$&</span>'));
	};

	$scope.candiate_matched = [];
	$scope.relevant_skills = [];
	$scope.loading = false;

	$scope.submit_search = function () {
		var skills = [];
		$scope.loading = true;
		$scope.candiate_matched = [];

		$scope.searchSkills.forEach(function (i) {
			skills.push(i.text)
		});

		skills = skills.join();

		$http.get('/api/v1/matching_candidates?skills=' + skills + '&limit=' + $scope.limit).then(function(data) {
			$scope.candiate_matched = data.data;
			console.log(data.data);
			$scope.loading = false;
		});

		$http.get('/api/v1/relevant_skills?skills=' + skills).then(function(data) {
			$scope.relevant_skills = data.data;
		});
	}
});