Title: Converting to the Angular HttpClient
Date: 2017-09-11 22:50
Tags: code, angular, tdd
Authors: Jonathan Sharpe
Summary: A summary of the experience of converting a simple Angular project from Http to the new HttpClient

As I mentioned in [a previous article][1], Angular 4.3 introduced a new API for
making HTTP calls, supplementing the `HttpModule` in `@angular/http` with the 
new `HttpClientModule` in `@angular/common/http`. I experimented with the new
interceptors and request progress API, but didn't actually try it out in a
working application.

So below is the results of an experiment to switch an existing project, [Salary
Stats][2], over to the `HttpClient` and test drive the new API for both the
client and the tests. Despite the clear warnings in the documentation I'm using
the Angular [in-memory web API][5] to allow the user to make CRUD operations
without setting up a backend; this needed an upgrade to v0.4.0 to support the
new client.

## Setup

Firstly, there's configuration. Using `Http`, the best way to test a service
was to replace the `ConnectionBackend` with a special `MockBackend` that
provides access to active connections. Using Angular's dependency injection
(DI) through the `TestBed`, this was reasonably straightforward:

```typescript
beforeEach(() => {
  TestBed.configureTestingModule({
    providers: [
      { provide: ConnectionBackend, useClass: MockBackend },
      { provide: RequestOptions, useClass: BaseRequestOptions },
      Http,
      PersonService,
    ]
  });

  service = TestBed.get(PersonService);
  backend = TestBed.get(ConnectionBackend);
});
```

The `Http` class has two injected dependencies, so we can either import the
whole `HttpModule` and override `ConnectionBackend` or just provide both
directly. Things are much simpler with the `HttpClientTestingModule`, however,
which can be added to the `imports` array and will mock everything for you:

```typescript
beforeEach(() => {
  TestBed.configureTestingModule({
    imports: [HttpClientTestingModule],
    providers: [PersonService],
  });

  service = TestBed.get(PersonService);
  httpMock = TestBed.get(HttpTestingController);
});

afterEach(() => {
    httpMock.verify();
})
```

Now instead of the `MockBackend` we get access to the `HttpTestingController`,
which gives access to a more synchronous API; rather than subscribing to a
stream of connections you can assert on the existence of specific requests,
flush them with a response as needed then verify that no unexpected requests
have been made.

## Checking the request

A simple first test for a new service method would be to check that it's making
the appropriate request to the backend.

```typescript
it('should get the people from the API', done => {
  backend.connections.subscribe((connection: MockConnection) => {
    expect(connection.request.url).toMatch(/\/people$/);
    expect(connection.request.method).toBe(RequestMethod.Get, 'expected GET request');
    done();
  });

  service.fetch();
});
```

Rewriting this with the new test API:

```typescript
it('should get the people from the API', () => {
  service.fetch();

  httpMock.expectOne('/app/people');
});
```

This demonstrates the value of the synchronous API; no more worrying about the
`DoneFn` and which order to make the request and set up the expectations.
Personally I find the second version much more readable, as it's a better fit
for the common *"Arrange, Act, Assert"* (or *"Given, When, Then"*) testing
pattern.

Sadly, one thing that seems to be missing here is the ability to provide a
regular expression to match the request URL. We have found this very useful in
combination with the Angular CLI's environment settings, allowing us to use
different profiles for local testing and our various deployment environments,
without the root URLs bleeding into the test setup.

Instead, you can match just the request method to get access to the
`TestRequest`:

```typescript
const req  = httpMock.expectOne({ method: 'GET' });
expect(req.request.url).toMatch(/\/people$/);
```

Also note that the API now uses string representations of the request method
rather than the enumerator I mentioned in [*Testing async data in Angular*][3];
*"Expected 'GET' to be 'POST'."* is a definite improvement over *"Expected 0 to
be 1."*, although you don't get the IDE support to autocomplete it.

## Testing with response data

The next test would drive out what happens with the data in the response. As
the new client parses the JSON for you by default you may not need to do
anything further, but in this case I want the raw object converted to a class
with some business logic in it.

```typescript
it('should expose the people as an observable', done => {
  let people = [{ name: 'Alice', salary: 12345, cohort: 'A' }];

  backend.connections.subscribe((connection: MockConnection) => {
    connection.mockRespond(new Response(new ResponseOptions({
      status: 200,
      body: { data: people },
    })));
  });

  service.fetch();

  service.people$.subscribe(received => {
    expect(received).toEqual([new Person(people[0].name, people[0].salary, people[0].cohort)]);
    done();
  });
});
```

I have generally been avoiding testing the request and the response handling in
the same method because that leads to having assertions before *and* after the
point at which the action is taken, which seems very confusing (*"Arrange &
Assert, Act, Assert Again"*?) But with the new API, the assertions all come
after the action:

```typescript
it('should expose the people as an observable', done => {
  const people = [{ name: 'Alice', salary: 12345, cohort: 'A' }];

  service.fetch();

  const req = httpMock.expectOne({ method: 'GET' });
  expect(req.request.url).toMatch(/\/people$/);
  req.flush({ data: people });

  service.people$.subscribe(received => {
    expect(received).toEqual([new Person(people[0].name, people[0].salary, people[0].cohort)]);
    done();
  });
});
```

Given that some expectation on the request is needed to get access to the
`TestRequest` to `flush` the response data through it, and given that this all
happens *after* the service call, it now seems sensible to combine two tests
into a single one.

The `DoneFn` is still required, because I'm exposing the data over an
observable as discussed in [*Handling data with the Angular AsyncPipe*][4], but
the HTTP part of the test is still handled synchronously. `people$` has replay
behaviour in this case, so we can subscribe after the service call and still
receive the latest data.

## Testing a POST

The in-memory web API also provides create and delete functionality.

```typescript
it('should post a new person to the API', done => {
  let name = 'Lynn';
  let salary = 123;
  let cohort = 'Q';

  backend.connections.subscribe((connection: MockConnection) => {
    expect(connection.request.url).toMatch(/\/people$/);
    expect(connection.request.method).toBe(RequestMethod.Post, 'expected POST request');
    expect(connection.request.json()).toEqual({ name, salary, cohort });
    done();
  });

  service.addPerson(new Person(name, salary, cohort));
});
```

Converting this to the new testing API is reasonably straightforward again,
giving the test much clearer structure:

```typescript
it('should post a new person to the API', () => {
  let name = 'Lynn';
  let salary = 123;
  let cohort = 'Q';

  service
      .addPerson(new Person(name, salary, cohort))
      .subscribe(() => {});

  const req = httpMock.expectOne({ method: 'POST' });
  expect(req.request.url).toMatch(/\/people$/);
  expect(req.request.body).toEqual({ name, salary, cohort });
});
```

One big gotcha here is that `HttpClient.post`, unlike `Http.post`, seems to be
a *cold* observable; you need to `subscribe` for the request to actually take
place. This may mean refactoring usages of these methods if you aren't already
returning and subscribing to the request observable.

## Service implementation

For the POSTs and DELETEs not much changed, I just had to replace `private
http: Http` with `private http: HttpClient` and the code continued to work
perfectly; the generic types on request methods are optional, and if you're not
dealing with a response you can ignore them completely. Actually using the
generic types, and with the default JSON unwrapping, the `fetch` method went
from:

```typescript
fetch() {
  this.http
      .get(this.personRoute)
      .subscribe(response => {
        this.personSubject.next(this.deserialise(response.json().data));
      });
}
```

to:

```typescript
fetch() {
  this.httpClient
      .get<{ data: RawPerson[] }>(this.personRoute)
      .subscribe(json => {
        this.personSubject.next(this.deserialise(json.data));
      });
}
```

A subtle improvement, but it helps to document your expectations of the API and
means you get IDE support for the resulting object.

## `Http` or `HttpClient`?

For new code, adopting the `HttpClient` is a no-brainer; even [the
documentation][6] has been switched over. So the big question is, is it worth
switching an application over to `HttpClient`? In the application code, the
switching process is not terribly complicated; anything that doesn't involve
the response may already work. And if you *are*, the new API will likely allow
you to remove a bunch of `.json()` calls and benefit from better type support.

The downside is that the new testing API, much as I prefer it to the previous
system, means a lot of test refactoring. And as much of your code will already
be working, using a technique like [*"refactoring against the red bar"*][7]
means you may spend a while breaking working code to ensure that the refactored
tests will fail in a useful way. So, unless you need some of the new
functionality (the interceptors seem particularly useful), it is probably not
worth the conversion unless:

  - you're still in the earlier stages of development, so you're likely to get
    the benefits in the additional services you write; or

  - you're planning to keep upgrading Angular into v5 (`@angular/http` is
    deprecated from [5.0.0-beta.6][8]).

See the full commit switching `salary-stats` over to the new API [here][9].

  [1]: {filename}/development/angular-http-client.md
  [2]: https://github.com/textbook/salary-stats
  [3]: {filename}/development/async-angular-tests.md
  [4]: {filename}/development/async-angular-data.md
  [5]: https://www.npmjs.com/package/angular-in-memory-web-api
  [6]: https://angular.io/guide/http
  [7]: http://corgibytes.com/blog/2016/09/20/refactoring-against-the-red-bar/
  [8]: https://github.com/angular/angular/blob/fa6b802be4c79f57aa8484fe47f0c860f1226683/CHANGELOG.md#features
  [9]: https://github.com/textbook/salary-stats/commit/046cfb059dd1b7e141141ef018a8ee029232221c
