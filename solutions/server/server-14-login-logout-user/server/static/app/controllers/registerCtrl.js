app.controller('registerCtrl', function ($scope, $location, AuthService, TaskService) {

    if (AuthService.isLoggedIn()) {
      $location.path('/');
    }

    $scope.register = function () {

      // initial values
      $scope.error = false;
      $scope.disabled = true;

      // call register from service
      AuthService.register($scope.registerForm.email,
                           $scope.registerForm.password)
        // handle success
        .then(function () {
          AuthService.login($scope.registerForm.email,
                             $scope.registerForm.password)
            .then(function() {
              TaskService.loadLists(false)
                .then(function(){
                  // initially load tasks
                  debug(TaskService.lists)
                  TaskService.lists.forEach(function(list) {
                    TaskService.loadTasks(false, list.id);
                  });
                  $location.path('/');
                  $scope.disabled = false;
                  $scope.loginForm = {};
                });
            })
            .catch(function() {
              $location.path('/login');
              $scope.disabled = false;
              $scope.registerForm = {};
            })
        })
        // handle error
        .catch(function (response) {
          $scope.error = true;
          $scope.errorMessage = "Ooops! Something went wrong =(";
          $scope.disabled = false;
          $scope.registerForm = {};
        });
    };
});
