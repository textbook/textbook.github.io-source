Title: Testing async data in Angular
Date: 2017-04-16 15:00
Modified: 2017-07-15 20:30
Tags: code, angular, typescript, rxjs, tdd
Authors: Jonathan Sharpe
Summary: Using the Angular TestBed to test asynchronous API data manipulation.

 > This post is a follow up to [Handling data with the Angular AsyncPipe][1], 
 > and assumes you're familiar with the service and component used there.

In a previous article I outlined a way to use the asynchronous nature of 
`Http`-based services to handle streams of data right through to the template. 
One of the core practices of the Extreme Programming methodology we use at 
Pivotal is test-driven development (TDD), so I thought it would also be helpful 
to show how we've approached writing our tests.

Angular comes with some useful built-in functionality to enable testing; see 
[their article][2] on the subject for more information. We're also using 
Jasmine's [asynchronous support][6], calling `done()` to explicitly define when
a test is considered finished.

## Testing the service

Angular includes a [`MockBackend`][3] that we can inject into the `Http`
created for the service to give access to the connections it's creating,
exposing an interface for testing and isolating tests from the actual network.

    :::typescript
    describe('RandomUserService', () => {
      let service: RandomUserService;
      let backend: MockBackend;
      
      beforeEach(() => {
        TestBed.configureTestingModule({
          providers: [
            { provide: ConnectionBackend, useClass: MockBackend },
            { provide: RequestOptions, useClass: BaseRequestOptions },
            Http,
            RandomUserService,
          ],
        });
        
        service = TestBed.get(RandomUserService);
        backend = TestBed.get(ConnectionBackend);
      });

      it('should make a GET to the API on fetch', done => {
        backend.connections.subscribe((connection: MockConnection) => {
          expect(connection.request.url).toEqual('https://randomuser.me/api/');
          expect(connection.request.method)
            .toEqual(RequestMethod.Get, 'expected GET request');
          done();
        });
        
        service.fetchRandomUser();
      });
    
      it('should expose the first result from the response', done => {
        let expectedUser = { name: { first: 'Alice' } };
        
        backend.connections.subscribe((connection: MockConnection) => {
          connection.mockRespond(new Response(new ResponseOptions({
            status: 200,
            body: { results: [expectedUser] },
          })));
        });
        
        service.fetchRandomUser();
        
        service.randomUser$.subscribe(user => {
          expect(user).toEqual(expectedUser);
          done();
        });
      });
    });

This allows us to test both:

 1. *That the request is correct*: we can check the URL, request method and 
    other properties to ensure that the settings are correct. Note the 
    non-default message on the method assertion; `RequestMethod` is an enum, 
    and e.g. *"Expected 0 to be 1."* isn't a very useful failure message.

 2. *That the response handling is correct*: in this case, that the first
    entry in the response JSON's `results` value is exposed over the 
    observable.
    
Note another advantage of the subject/observable formulation over the original
version here; as the subscription to `http.get(...)` happens inside the fetch
method, you don't need to subscribe to the result in the first test, where the
response is irrelevant. In cases where the request observable is returned from 
the service, *no request is made* unless the caller subscribes to it; GET is a
cold observable (however e.g. POST and PUT are hot, so you don't need to
subscribe unless you are actually interested in the result).
    
## Testing the component

As components include templates, which must be compiled, the testing is 
slightly more complex. The compilation is asynchronous, so the 
[Angular CLI][4] creates components with a test setup like the following: two
`beforeEach` calls, one with `async` to run the compilation, then a second
synchronous call where the fixture is created.
    
    :::typescript
    describe('RandomUserComponent', () => {
      let component: RandomUserComponent;
      let fixture: ComponentFixture<RandomUserComponent>;
      let serviceSpy: RandomUserService;
      let userSubject = new ReplaySubject<User>(1);
    
      beforeEach(async(() => {
        serviceSpy = jasmine.createSpyObj('RandomUserService', ['fetchRandomUser']);
        serviceSpy.randomUser$ = userSubject.asObservable();
    
        TestBed.configureTestingModule({
          providers: [
            { provide: RandomUserService, useValue: serviceSpy },
          ],
          declarations: [RandomUserComponent],
        }).compileComponents();
      }));
    
      beforeEach(() => {
        fixture = TestBed.createComponent(RandomUserComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
      });
    
      it('should fetch and render a random user', () => {
        let firstName = 'Alice';
        userSubject.next({ name: { first: firstName } });
        fixture.detectChanges();
    
        expect(serviceSpy.fetchRandomUser).toHaveBeenCalled();
        expect(fixture.nativeElement.querySelector('span').innerText).toEqual(firstName);
      });
    });
    
    
Note that the subject/observable usage in the test mirrors that in the actual
service implementation; this means that new data can be pushed into the test at 
any time. You can also do this when setting up tests for the original version
of the service:

    :::typescript
    service = jasmine.createSpyObj('RandomUserService', ['getRandomUser']);
    (service.getRandomUser as Spy).and.returnValue(userSubject.asObservable());

In both cases making the `service` explicitly typed as a `RandomUserService` 
means that the IDE and compiler can tell us if the wrong field and method names 
are used; e.g. if I'd mistyped the assignment of the observable:

    TS2339: Property 'randomUsers$' does not exist on type 'RandomUserService'.

## Testing more complex components

The nice things about the `TestBed` and `ComponentFixture` model are that it 
allows us to:

 1. *Be very specific about the dependencies of our components*: its hooks into
    dependency injection system allow use to provide test doubles as required, 
    and either:
    
     - explicitly provide required sub-components (real or fake) to test 
       interactions; or 
     
     - use the `NO_ERRORS_SCHEMA` to ignore missing sub-components and test a 
       single component in isolation.

 2. *Test interactions between the class and template*: it exposes the 
    interface between the two parts of the component. For example, imagine the 
    following component:
    
        :::typescript
        @Component({
          selector: 'fetch-trigger',
          template: '<button (click)="triggerFetch()"></button>',
        })
        export class FetchTriggerComponent {
          constructor(private service: RandomUserService) { }
          
          triggerFetch() {
            this.service.fetchRandomUser();
          }
        }
        
    It's pretty straightforward to unit test that calling the `triggerFetch` 
    method invokes the appropriate service method, but given a correctly 
    configured `TestBed` you can also test that clicking the button in the HTML 
    calls `triggerFetch`. Better still, to write a test less tied to the 
    current implementation, you can test *across* the boundary that clicking 
    the button calls `fetchRandomUser` on a stub of the service.
    
        :::typescript
        it('should fetch a random user when the button is clicked', () => {
          component.nativeElement.querySelector('button').click();
          
          expect(serviceSpy.fetchRandomUser).toHaveBeenCalled();
        });
    
## Testing service error handling

One gotcha we've come across is with handling 4xx and 5xx response status codes 
in `Http`-based services. Introducing error handling into the component is as 
simple as providing the second callback to subscribe:

    :::typescript
    .subscribe(
        user => this.userSubject.next(user),
        error => {
          if (error instanceof Response) {
            this.errorSubject.next(error.status);
          }
        }
    );

Naïvely, you might think that testing it is a simple matter of responding from 
the mock backend with an error code:

    :::typescript
    it('should expose errors', done => {
      service.error$.subscribe(status => {
        expect(status).toBe(404);
        done();
      });
  
      backend.connections.subscribe((connection: MockConnection) => {
        connection.mockResponse(new Response(new ResponseOptions({
          status: 404,
        })));
      });
  
      service.fetchRandomUser();
    });
    
*(Note that, as we're not using a `ReplaySubject` for errors to avoid 
replaying them after the fact, you need to `.subscribe` *before* triggering the 
response.)* 

However, this will end with:

    
    Error: Timeout - Async callback was not invoked within timeout specified by jasmine.DEFAULT_TIMEOUT_INTERVAL.
    
Instead, you may try to use another method on the connection: `mockError`. This 
time the TypeScript compiler has something to say:

    TS2345: Argument of type 'Response' is not assignable to type 'Error'.

It turns out that, unlike `mockRespond` and `mockDownload`, the `mockError` 
method takes an `Error` rather than a `Response`. In practice, however, the
`error` on the second subscribe callback is `any`, and will be a `Response`
in the case of a 4xx or 5xx response code. To get around this, you can adopt
the suggestion from [this comment on the Angular GitHub repo][5]:

    :::typescript
    class MockError extends Response implements Error {
        name: any;
        message: any;
    }

which allows you to call `mockError` and still test for `Response` in the error
callback in the service:

    :::typescript
    it('should expose errors', done => {
      service.error$.subscribe(status => {
        expect(status).toBe(404);
        done();
      });
  
      backend.connections.subscribe((connection: MockConnection) => {
        connection.mockError(new MockError(new ResponseOptions({
          status: 404,
        })));
      });
  
      service.fetchRandomUser();
    });
 
There are a few open issues related to this behaviour, so hopefully it will be 
fixed at some point in the near future.

 > **Update**: as of 4.3.0 the new `HttpClient` module seems to deal with this
 > more neatly, providing an official equivalent of `MockError`; see [New to
 > Angular 4.3: HttpClient][7] for more information.
 
  [1]: {filename}/development/async-angular-data.md
  [2]: https://angular.io/docs/ts/latest/guide/testing.html
  [3]: https://angular.io/docs/ts/latest/api/http/testing/index/MockBackend-class.html
  [4]: https://cli.angular.io/
  [5]: https://github.com/angular/angular/pull/8961#issuecomment-251549757
  [6]: https://jasmine.github.io/2.5/introduction#section-Asynchronous_Support
  [7]: {filename}/development/angular-http-client.md
