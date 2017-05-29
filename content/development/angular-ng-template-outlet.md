Title: ngTemplateOutlet tricks
Date: 2017-05-29 15:30
Tags: angular, html
Authors: Jonathan Sharpe
Summary: Using an Angular ngTemplateOutlet to bind child content from the parent template.

I mentioned in [a previous article][1] that the limitations of projecting
content from a parent element to its child element, for example:

```html
<!-- template -->
<ng-content></ng-content>

<!-- usage -->
<my-component>
  <p>I am a paragraph.</p>
</my-component>

<!-- result -->
<p>I am a paragraph.</p>
```

were that you can't repeat the projection multiple times or access properties
on the child class from the parent template. However, one of
[Günter Zöchbauer][2]'s *many* contributions to the Angular community on Stack
Overflow is [this answer][3] outlining how the [`ngTemplateOutlet`][4] can be
used to do this. It's somewhat more complex than simply adding an `ng-content`
element, but allows for more complex behaviour too.

---

To give a more specific case, imagine you're writing an autocomplete input,
where suggestions are fetched as the user types and shown beneath the text box.
A simple approach might define the child template like this:

```html
<div>
  <input>
  <div class="suggestions">
    <div class="suggestion" *ngFor="let suggestion of suggestions">
      <h2>{{ suggestion.name }}</h2>
      <p>{{ suggestion.email }}</p>
    </div>
  </div>
</div>
```

This is limiting, though; the structure of each suggestion is fixed, making the
component less reusable. It would be more flexible if we could define the
suggestion template in the parent component then inject each `suggestion` into
it to provide the display values.

Accessing an `ng-template` defined in the parent template as follows:

```typescript
@Component({
  selector: 'my-child',
  ...
})
export class ChildComponent { 
  @ContentChild(TemplateRef) parentTemplate;

  suggestions: { name: string, email: string }[] = [...];
}
```

and using an `ngTemplateOutlet` to render it out, with the child template
defined as:

```html
<div>
  <input>
  <div class="suggestions">
    <div *ngFor="let suggestion of suggestions">
      <ng-container *ngTemplateOutlet="parentTemplate; context: { $implicit: suggestion }">
      </ng-container>
    </div>
  </div>
</div>
```

allows you to provide the structure of each suggestion in the parent, but using
the `suggestion` variable defined in the `ngFor` loop in the child:

```html
<my-child>
  <ng-template let-suggestion>
    <div class="suggestion">
      <h2>{{ suggestion.name }}</h2>
      <p>{{ suggestion.email }}</p>
    </div>
  </ng-template>
</my-child>
```

The key points here are:

 - Using the [`ContentChild`][5] with [`TemplateRef`][6] in the child to access
   the `ng-template` element defined in the parent;

 - Providing a `context` to inject into the template and binding the
   `suggestion` variable to the `$implicit` key to make that the default value
   of the context; and

 - Placing `let-suggestion` on the parent's `ng-template` element to bind that
   default value context to the name `suggestion` in the parent (you can also
   use `let-nameInParent="nameInContext"` to bind non-default context values;
   `let-nameInParent` without a value is effectively shorthand for
   `let-nameInParent="$implicit"`).

Here is the above example as a Plunkr so you can play with it:

<iframe src="https://embed.plnkr.co/QNUe6R/?show=child,preview" 
        frameborder=0 
        width="100%" 
        height="400px">
</iframe>

---

The downside of this is that the parent needs to have a specific layout; it has
to define an `ng-template` with the appropriate `let-` attribute to gain access
to the child property. If you read the previous article, you may be thinking
that an `ng-template` with an attribute on it looks exactly like the de-sugared
versions of structural directives. I thought the same thing, and wondered if I
could write a structural directive of my own that would be applied as follows:

```html
<my-child>
  <div class="suggestion" *suggestion>
    <h2>{{ suggestion.name }}</h2>
    <p>{{ suggestion.email }}</p>
  </div>
</my-child>
```

and would generate the appropriate template in a simplified way. Sadly, it
seems like you can't access the actual template element from the directive, as
it never gets rendered. A no-op directive as follows:

```typescript
@Directive({
  selector: '[suggestion]',
})
export class SuggestionDirective { }
```

*can* be used to simplify the markup slightly:

```html
<my-child>
  <div class="suggestion" *suggestion="let suggestion">
    <h2>{{ suggestion.name }}</h2>
    <p>{{ suggestion.email }}</p>
  </div>
</my-child>
```

but you still need to explicitly include the `let`. I am yet to figure out how
to get around this (or if you even can).

  [1]: {filename}/development/angular-ng-elements.md
  [2]: https://stackoverflow.com/users/217408/g%C3%BCnter-z%C3%B6chbauer
  [3]: https://stackoverflow.com/a/37676946/3001761
  [4]: https://angular.io/docs/ts/latest/api/common/index/NgTemplateOutlet-directive.html
  [5]: https://angular.io/docs/ts/latest/api/core/index/ContentChild-decorator.html
  [6]: https://angular.io/docs/ts/latest/api/core/index/TemplateRef-class.html
