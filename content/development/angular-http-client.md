Title: New to Angular 4.3: HttpClient
Date: 2017-07-15 20:30
Modified: 2017-10-13 14:40
Tags: angular, html
Authors: Jonathan Sharpe
Summary: The latest version of Angular includes a new HTTP client, with a new API.

I recently discovered from [A Taste From The New Angular HTTP Client][1] (via 
[ng-newsletter][2], which covers both Angular and AngularJS) that Angular 4.3,
which [just became available][3], includes a new HTTP client. 


So what does it add?

 1. **JSON by default** - no more `.map(response => response.json())`; unless
    you explicitly specify e.g. `{ responseType: 'text' }` when making a
    request, the client will automatically parse the response body as JSON for
    you. You can still get the response, using `{ observe: 'response' }`, if
    you need access to e.g. the headers.
   
 2. **Response typing** - versions of the requests methods that use generic
    types are now provided, so you can supply a type for the return value:
    
        this.http.get<Thing>('/api/thing').subscribe(thing => ...)
 
 3. **Interception** - the new `HttpInterceptor` interface allows you to easily
    intercept requests and responses, without needing to extend the whole
    `Http` class yourself.
   
 4. **Progress reporting** - specify `{ reportProgress: true }` when making a
    request, and the client will give periodic updates on the upload or download
    progress.
   
 5. **Client testing module** - now you can simply add `HttpClientTestingModule`
    to your test bed's imports, instead of setting up the `MockBackend`
    yourself. It also provides a new API, which looks like a more synchronous
    approach to testing.
    
 6. **Proper error response** - as I mentioned in [Testing async data in 
    Angular][8], it used to be tricky to test error responses (e.g. 404)
    because the `mockError` method took an `Error`, not a `Response`. As a
    workaround, I showed how to create a new class that combines the two.
    However, that's now provided as part of the module:
  
        export class HttpErrorResponse extends HttpResponseBase implements Error { ... }
        
    Hopefully this will make error handling neater and testing easier.

As I'd also been playing with [`@angular/material`][4], I thought I'd combine 3
and 4 to create an automatically-updated progress bar, which shows the progress
of the current request. First, I had to write an interceptor:

```typescript
@Injectable()
export class ProgressInterceptor implements HttpInterceptor {
  public progress$: Observable<number | null>;
  private progressSubject: Subject<number | null>;

  constructor() {
    this.progressSubject = new ReplaySubject<number | null>(1);
    this.progress$ = this.progressSubject.asObservable();
  }

  intercept<T>(req: HttpRequest<T>, next: HttpHandler): Observable<HttpEvent<T>> {
    const reportingRequest = req.clone({ reportProgress: true });
    const handle = next.handle(reportingRequest);

    return handle.do((event: HttpEvent<T>) => {
      switch (event.type) {
        case HttpEventType.Sent:
          this.progressSubject.next(null);
          break;
        case HttpEventType.DownloadProgress:
        case HttpEventType.UploadProgress:
          if (event.total) {
            this.progressSubject.next(Math.round((event.loaded / event.total) * 100));
          }
          break;
        case HttpEventType.Response:
          this.progressSubject.next(100);
          break;
      }
    });
  }
}
```

This does two main things:

  - `.clone` the request object, setting the progress reporting flag. Most of
    the objects in the client are immutable, but provide helper methods to
    create new instances with updated configuration.
    
  - `.subscribe` to the events coming out of the handler. It switches on the
    type of the event to determine the start of the request, progress updates
    and the arrival of the response. At each step it sends updates using the 
    *"public observable, private subject"* pattern I discussed in [Handling
    data with the Angular AsyncPipe][7].

I then wrote a simple wrapper around the [`<md-progress-bar>`][5], exposing its
basic styling while hiding the other details of the API (the [string literal
types][6] for mode and colour are defined in but not exposed by the Angular
Material package, so I recreated them):

```typescript
export type ProgressBarColor = 'primary' | 'accent' | 'warn';

type ProgressBarMode = 'determinate' | 'indeterminate' | 'buffer' | 'query';

@Component({
  selector: 'pgs-progress-bar',
  template: `
    <md-progress-bar [value]="progressPercentage$ | async"
                     [color]="color">
    </md-progress-bar>
  `,
})
export class ProgressComponent implements OnInit {
  @Input() color: ProgressBarColor = 'primary';

  @ViewChild(MdProgressBar) private progressBar: MdProgressBar;

  progressPercentage$: Observable<number>;

  constructor(private interceptor: ProgressInterceptor) { }

  ngOnInit() {
    this.progressPercentage$ = this.interceptor.progress$
        .map(progress => {
          if (progress === null) {
            this.setMode('indeterminate');
            return 0;
          } else {
            this.setMode('determinate');
            return progress;
          }
        });
  }

  private setMode(mode: ProgressBarMode) {
    this.progressBar.mode = mode;
  }
}
```

This puts the progress bar into "indeterminate" mode, where it just shows that
*something* is going on, if it receives `null` from the interceptor. If it
receives a number, that's used as the value for current progress and the bar is
switched into "determinate" mode, where it fills up from 0 to 100.

Finally I wrote a module to glue the two classes together and add the actual
Angular Material progress bar:

```typescript
const interceptor = new ProgressInterceptor();

@NgModule({
  imports: [
    BrowserModule,
    HttpClientModule,
    MdProgressBarModule,
  ],
  declarations: [
    ProgressComponent,
  ],
  providers: [
    { provide: ProgressInterceptor, useValue: interceptor },
    { provide: HTTP_INTERCEPTORS, useValue: interceptor, multi: true },
  ],
  exports: [
    ProgressComponent,
  ]
})
export class ProgressModule { }
```

Note that I create a single instance of the interceptor, which is then both
used in the `HTTP_INTERCEPTORS` array and provided directly under its own name.
If I'd used `useClass: ProgressInterceptor` then the client would have been
using a different instance from the one in the component, and the progress bar
would never get updated.

Now you can drop `<pgs-progress-bar></pgs-progress-bar>` anywhere into the
application and it will show the status of the latest request made through the
`HttpClient`, with no need for any additional wiring. You can also inject the
`ProgressInterceptor` into anything else that needs to keep track of request
progress.

This is just a toy implementation (one obvious issue: what if there are two
parallel requests?) but hopefully shows what's possible with the new API. Note
that the old client (in `@angular/http`) isn't going away just yet; the new one
is available in parallel (in `@angular/common/http`) for the time being.

 > **Update**: an earlier version of this article both subscribed to *and* 
 > returned the `handle` from the interceptor - as VerSo pointed out in the 
 > comments (thanks!), this would mean that the request got made twice.

  [1]: https://netbasal.com/a-taste-from-the-new-angular-http-client-38fcdc6b359b
  [2]: https://www.ng-newsletter.com/
  [3]: http://angularjs.blogspot.co.uk/2017/07/angular-43-now-available.html
  [4]: https://material.angular.io/
  [5]: https://material.angular.io/components/progress-bar
  [6]: https://www.typescriptlang.org/docs/handbook/advanced-types.html#string-literal-types
  [7]: {filename}/development/async-angular-data.md
  [8]: {filename}/development/async-angular-tests.md
