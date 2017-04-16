Title: Handling data with the Angular AsyncPipe
Date: 2017-04-09 15:20
Modified: 2017-04-16 15:00
Tags: code, angular, typescript, rxjs
Authors: Jonathan Sharpe
Summary: Patterns for manipulating API data asynchronously using RxJS Observables in Angular. 

In my current project at work, we're using [Angular][6] to build the front end 
of a web application that gives the user a dashboard of useful information. As 
part of this we've adopted a few patterns for handling data that I thought 
would be useful to others. 

## Asynchronous data sources

Say we want to get a random person from [randomuser.me][3], so that we can show 
their first name. We might start with a service that looks like:

    :::typescript
    @Injectable()
    export class RandomUserService {
      constructor(private http: Http) { }
      
      getRandomUser() {
        return this.http
          .get('https://randomuser.me/api/')
          .map(response => response.json().results[0]);
      }
    }

In our component we then `.subscribe` to the resulting observable and assign 
the data to a field:

    :::typescript
    @Component({
      selector: 'random-user',
      template: '<span>{{ user.name.first }}</span>',
    })
    export class RandomUserComponent {
      user;
      
      constructor(private service: RandomUserService) { }
      
      ngOnInit() {
        this.service.getRandomUser()
          .subscribe(user => this.user = user);
      }
    }

However, you quickly run into issues; prior to the GET call resolving via the 
subscription, `this.user` is `null`, so getting the appropriate fields from it 
fails:

    TypeError: Cannot read property 'name' of null ...

and the view doesn't render at all. 

## Simple solutions

To avoid this, you could set a default value, so that the appropriate fields 
always exist:

    :::typescript
    user = { name: { first: 'Alice' } };

However, it's not always obvious what an appropriate default would be, and if 
the request fails the end user is potentially stuck looking at some dummy data. 

Alternatively we can use [the safe navigation operator][5] to resolve each 
field:

    :::html
    <span>{{ user?.name?.first }}</span>

but that's not too neat and is prone to human error.

## Leveraging observables

Instead, we can use the `AsyncPipe` to resolve the value asynchronously from 
the service:

    :::html
    <span>{{ firstName$ | async }}</span>
 
*(The convention of a dollar sign suffix to indicate an observable was 
apparently [popularised by Cycle.js][7].)*

In the component, this can be implemented as a property:

    :::typescript
    get firstName$() {
      return this.service.randomUser$
        .map(user => user.name.first);
    }

In the service, we've been using a *"public observable, private subject"* 
pattern:

    :::typescript
    @Injectable()
    export class RandomUserService {
      private userSubject = new ReplaySubject(1);
      
      randomUser$ = this.userSubject.asObservable();
      
      constructor(private http: Http) { }
      
      fetchRandomUser() {
        this.http
          .get('https://randomuser.me/api/')
          .map(response => response.json().results[0])
          .subscribe(user => this.userSubject.next(user));
      }
    }

Using a `ReplaySubject` means that new subscribers, joining after a fetch, 
still get the latest value. Keeping it private means that the subscribers can't 
push new data into it, so we know any new state must come from within the 
service itself. Any component can trigger a new request via the public 
`fetch...` method, and all subscribers then get the newest data as it arrives. 

## Combining data sources

In a few cases, we want to combine multiple requests (for example, to draw a 
graph using data from two API endpoints). Initially this seemed quite tricky, 
as we wouldn't necessarily know when both requests had resolved. However, RxJS 
provides `combineLatest` for this purpose:

    :::typescript
    ngOnInit() {
      this.combinedData$ = Observable.combineLatest(
        service.someData$,
        service.otherData$,
        (some, other) => this.combine(some, other)  // or "this.combine.bind(this)"
      );
    }

See e.g. [RxMarbles][4] for a demonstration of what this operator does, as well 
as other operators that can be applied to your streams of data. 

## Gotchas

Note a few problems we've run into:

 - `ExpressionChangedAfterItHasBeenCheckedError` on anything that passes `NaN` 
    into `| async`; I opened [an issue][1] about this and there's [a pull 
    request][2] to fix it. 
 - Exposing error states with a `ReplaySubject` can lead to some weird 
    behaviour; use a vanilla `Subject` instead, to avoid errors getting 
    replayed later. 
    
 > For more information on testing services and components written in this way, 
 > see the follow-up article [Testing async data in Angular][8].

  [1]: https://github.com/angular/angular/issues/15721
  [2]: https://github.com/angular/angular/pull/15723
  [3]: https://randomuser.me
  [4]: http://rxmarbles.com/#combineLatest
  [5]: https://angular.io/docs/ts/latest/guide/template-syntax.html#!%23safe-navigation-operator
  [6]: https://angular.io/
  [7]: https://cycle.js.org/basic-examples.html#basic-examples-increment-a-counter-what-is-the-convention
  [8]: {filename}/development/async-angular-tests.md
