In my program are 3 blocks of endpoints:

feedbacks:

- feedback/ - will show you all feedbacks of locations
- feedback/create/ - will create a feedback of some location(you can write comment and set 1-5 stars, also you can like or dislike comments)
- feedback/update/<int:pk>/ - you can edit your feedback
- feedback/delete/<int:pk>/ - you can delete your feedback

locations:

- locations/ - you can see all locations, also if you write paramaters you can search any locations with some text
- create/ - with this endpoint you can add some location
- update/<int:pk>/ - you can update info bout location
- delete/<int:pk>/ - you can delete some location(if there more time, here should add permission only to admin to do smth with locations info)
- location/<int:location_id>/ - here you can see more info bout locations
- filter-rating/<int:pk>/ - you can filter location with ratings(stars), that's will show locations where rating equal or above number you choose(1-5)
- filter-category/ - you can write category and you will see location which are in this category
- save_data/ - you can save all data in csv files

users:

- register/ - you can register
- login/ - you can login(and then you will have sessionId)
- logout/ - you can logout to login by another user
- protected/ - this endpoint was to check if session and mixin work correctly
- password_reset/ - you can reset your password(messege will sent to email you register with)
- password_reset/done/ - seccussful sent messege
- reset/<uidb64>/<token>/ - confirmation
- reset/done/ - finally reset


also there 1 endpoint for admin page:
- admin/ - you must create superuser to enter into admin menu


Also in my progect is template folder where locate a lot of html to simplier test(for me it's easier) 

And finally you can see json file with postman request. If you open this collection you can easily test my endpoints.