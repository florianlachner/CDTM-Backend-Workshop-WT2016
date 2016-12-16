app.controller('loginCtrl', function($scope, $location, AuthService, TaskService) {

  if (AuthService.isLoggedIn()) {
    $location.path('/');
  }

  $scope.login = function () {
    // initial values
    $scope.error = false;
    $scope.disabled = true;

    // call login from service
    AuthService.login($scope.loginForm.email, $scope.loginForm.password)
      // handle success
      .then(function () {

        TaskService.loadLists(false)
          .then(function(){
            // initially load tasks
            TaskService.lists.forEach(function(list) {
              TaskService.loadTasks(false, list.id);
            });
            $location.path('/');
            $scope.disabled = false;
            $scope.loginForm = {};
          });
      })
      // handle error
      .catch(function () {
        $scope.error = true;
        $scope.errorMessage = 'Invalid username and/or password';
        $scope.disabled = false;
        $scope.loginForm.password = null;
      });
  };
});
