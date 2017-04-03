var app = angular.module('app', ['ngTagsInput', 'ngAvatar', 'ngSanitize']);

app.controller('main', function ($scope, $http, $sce) {
	$scope.searchSkills = [ 'js' ];
	$scope.skillColor = {};
	$scope.limit = 20;
	$scope.candiate_matched = [];
	$scope.relevant_skills = [];

	$scope.skillTypeAhead = function (keyword) {
		return [];
	};

	// Profile URL
	$scope.profileURL = function (name) {
		return 'https://www.linkedin.com/search/results/index/?keywords=' + name;
	}

	$scope.highlightSkill = function(text) {
		var skills = [];
		$scope.searchSkills.forEach(function (i, index) {
			skills.push(i.text);
			var skill = i.text;
			$scope.skillColor[skill] = index;

			skill_search = [ skill ].concat($scope.getRelevantSkills(skill))
			skill_search = skill_search.join('|')

			text = text.replace(new RegExp(', (' + skill_search + '),', 'gi'), 
			', <span class="highlightedText color'+ index +'">$1</span>,')
		});
		return $sce.trustAsHtml(text);
	};

	$scope.getSkillColor = function (skill) {
		if (skill in $scope.skillColor) return $scope.skillColor[skill];
		return -1;
	}

	$scope.getRelevantSkills = function (skill) {
		for (var sk in $scope.relevant_skills) {
			if ($scope.relevant_skills[sk].name == skill)
				return $scope.relevant_skills[sk].data;
		}

		return [];
	}
	
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
			angular.forEach($scope.candiate_matched, function(value, index) {
				value['skills_html'] = value.skills;
			});

			$scope.loading = false;
		});

		$http.get('/api/v1/relevant_skills?skills=' + skills).then(function(data) {
			$scope.relevant_skills = data.data;
			angular.forEach($scope.candiate_matched, function(value, index) {
				value['skills_html'] = $scope.highlightSkill(value.skills)
			});
		});
	}
});