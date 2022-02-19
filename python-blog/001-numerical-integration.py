"""
Numerical Integration
---------------------

Here is an introduction to Numerical Integration with Python!
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

###############################################################################
# Let's look at a simple function:
#
# .. math::
#
#     g(x) = \sin(x)
#
# which we know the analytical integral as:
#
# .. math::
#
#     G(x) = - \cos(x)
#
# and let's integrate that from 0 to :math:`\frac{5\pi}{4}`. Analytically, this is:
#
# .. math::
#
#     \int_0^{\frac{5\pi}{4}} g(x) \, dx = - \cos(x) |_0^{\frac{5\pi}{4}} = - \cos(\frac{5\pi}{4}) + \cos(0) = \frac{\sqrt{2}}{2} + 1 = 1.7071

np.sqrt(2) / 2 + 1

###############################################################################
# We can visualize this as the area under the curve - which is all a numerical
# integral is; an approximation of the area under the curve.
# To do a numerical integration, we simply discretize our x space and then
# evaluate our function. Once we have that, we can sum the evaluation and
# multiply by the discretization factor to yield the effective area under the
# curve.
#
# So let's discretize :math:`g(x)` into several rectangles which we can use to
# solve for the area under this curve.


g = lambda x: np.sin(x)
a, b = 0, 5 * np.pi / 4

y = np.linspace(a, b)

dy = np.pi / 16
yy = np.arange(a, b, dy)


def plot_rects(xx, f, delta):
    for v in xx:
        value = f(v)
        if value >= 0.0:
            loc = 0.0
            h = value
        else:
            loc = value
            h = 0 - value
        r = mpl.patches.Rectangle(
            (v - delta / 2.0, loc), width=delta, height=h, edgecolor="k", linewidth=1
        )
        plt.gca().add_patch(r)
    return


def plot_g():
    plt.plot(y, g(y))
    plt.plot(yy, g(yy), "ro")

    plot_rects(yy, g, dy)

    plt.xlabel("$x$")
    plt.ylabel("$g(x)$")


plot_g()
plt.show()

###############################################################################
# So now we can sum the areas of all of those rectangles to get an
# approximation of the area under the curve (the integral)
np.sum(g(yy - (dy / 2)) * dy)


# That's not too bad considering our rectangles do not perfectly follow the
# curve. Let's now try choosing a :math:`\Delta x` value that will increase the
# sampling creating finer spaced rectangles to improve our approximation.

dy = np.pi / 32
yy = np.arange(a, b, dy)

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plot_g()
plt.title("Area = {:.3f}".format(np.sum(g(yy) * dy)))

plt.subplot(1, 2, 2)

dy = np.pi / 128
yy = np.arange(a, b, dy)

plot_g()
plt.title("Area = {:.3f}".format(np.sum(g(yy) * dy)))

plt.tight_layout()
plt.show()


###############################################################################

np.sum(g(yy) * dy)

###############################################################################
# Now that's much better! as we decrease the :math:`\Delta x` value, we see the
# approximation start to converge on the analytical answer for the integral.
# The rectangles appear to be consistently overestimating the integral.
#
# Integrating a Complex Function
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Now let's apply that concept to numerically integrate a more complex function
# such as:
#
# .. math::
#
#     f(x) = \sin(\frac{1}{x})
#
# from 0 to :math:`2\pi`. This allows us to really showcase where numerical
# integration benefits as I don't even know where to begin when it comes to
# analytically integrating that.

f = lambda x: np.sin(1 / x)

###############################################################################
# To do so, we'll need to define a range of x values on which to evaluate the
# function. Let's try out a few different sets of x values to plot the values
# of :math:`f(x)` to gain insight into how this function behaves.
#
# First, let's see what happens when we plot this function at linear intervals
# between 0 and :math:`2\pi` (note that we cannont have a division by zero, so our
# lower boound must be some small value, not 0: we'll use :math:`10^{-9}`.

num = 100000
zero = 1e-9

# Create an array of x values to evaluate
x = np.linspace(zero, 2 * np.pi, num)

# Evaluate and plot the values
plt.plot(x, f(x))
plt.xlabel("$x$")
plt.ylabel("$f(x)$")
plt.show()

###############################################################################
# Huh, that's weird. The function behaves quite differently from a typical :math:`\sin`
# function and we appear to see some sort of decay - let's look into that a bit
# more. *At what x value are we seeing a change from oscillatory behavior to
# a decay?*
#
# From visual inspection, it looks like some value above :math:`\frac{1}{\pi}`
# (0.318). Let's reevaluate the function from that x value onward.
# Then find the maximum and see what interval of :math:`\pi` is causing the change
# in behavior.

subset = np.linspace(0.3, 2 * np.pi, num)
subset[np.argmax(f(subset))] * np.pi

###############################################################################
# Aha! It appears that the x value of :math:`\frac{2}{\pi}` marks the start of
# decay. This makes sense because :math:`\sin(1/2/\pi) = \sin(\pi/2) = 1`

plt.plot(x, f(x), label="$f(x)$")
plt.plot(2.0 / np.pi, f(2.0 / np.pi), "ro", label=r"$x=\frac{2}{\pi}$")
plt.legend()
plt.xlabel("$x$")
plt.ylabel("$f(x)$")
plt.show()

###############################################################################
# So now we know that have a separation point in our function - this might come
# in handy later. as we may have to treat those two regions of the function
# separately when numerically integrating.
#
# Now, let's explore the jumbled up portion of the plot for very low x values.
# There appears to be some high frequency oscillation between -1 and 1, but we
# can't really tell. To do this, let's create an exponentially varying x
# space to evaluate our function which will bring out finer sampling for lower
# values and see how the function behaves as x approaches zero.

x = np.geomspace(1e-2, 2 * np.pi, num)

plt.plot(x, f(x))
plt.gca().set_xscale("log")
plt.xlabel("$x$")
plt.ylabel("$f(x)$")
plt.show()

###############################################################################
# Now that's cool! :math:`f(x)` appears to have increasing frequency as x
# approaches zero. This is quite different from a normal :math:`\sin` function where
# we don't see any frequency change at all. This frequency variation will
# definitely pose a challenge for our numerical integration as we will need to
# make sure we properly sample this signal without aliasing.
#
# Let's see if we can come up with an equation for capturing that frequency
# variation as something we can use to build out our values that we will use
# for the numerical integration.
#
# First, let's evaluate our function between integer changes in :math:`\pi` to see
# how :math:`f(x)` oscilates between -1 and 1. We know from above that the last
# value of 1 occurred at :math:`\frac{2}{\pi}`, so let's use decreasing values from
# there.

f(3.0 / np.pi)


###############################################################################
f(3.0 / (2.0 * np.pi))


###############################################################################
f(2.0 / (3 * np.pi))


###############################################################################
f(2.0 / (4 * np.pi))


###############################################################################
f(2.0 / (5 * np.pi))

###############################################################################
# So this is interesting. I'm seeing a weird pattern where :math:`\frac{2}{n \pi}`
# appears to oscillate :math:`f(x)` between -1 and 1. Let's test this out.

xx = lambda n: 2 / (n * np.pi)
nn = 65
n = np.arange(1, nn)
xn = xx(n)

plt.plot(xn, f(xn), "ro")
plt.plot(x, f(x))
plt.gca().set_xscale("log")
plt.xlabel("$x$")
plt.ylabel("$f(x)$")
plt.show()


###############################################################################
# It appears that the equation :math:`\frac{2}{n \pi}` captures the oscillatory
# behavior of :math:`f(x)` quite well! We see that it marks the minimums, maximums,
# and zero-cross points for every period of :math:`f(x)`. This is just what we need
# to effectively integrate :math:`f(x)`.
#
# To start integrating this function, we simply need to sample several times
# between values of :math:`n`. Doing so is as simple as bumping up the number of
# setting a step size in ``numpy``'s ``arange`` method. Let's use a step size of
# 0.25 as that will give us 4 values between each cross-over and the min/max
# point. Let's see if that gives us a visually pleasing approximation of our
# function.


def plot_f():
    plt.gca().set_xscale("log")
    plt.plot(x, f(x))
    plt.plot(xn, f(xn), "ro")

    for i, v in enumerate(xn):
        if i == len(xn) - 1:
            continue
        value = f(v)
        if value >= 0.0:
            loc = 0.0
            h = value
        else:
            loc = value
            h = 0 - value
        delta = abs(xn[i] - xn[i + 1])
        r = mpl.patches.Rectangle(
            (v - delta / 2, loc), width=delta, height=h, edgecolor="k", linewidth=1
        )
        plt.gca().add_patch(r)
    plt.xlabel("$x$")
    plt.ylabel("$f(x)$")
    return


###############################################################################

dx = 0.25
n = np.arange(1, nn, step=dx)
xn = xx(n)

plot_f()
plt.show()

###############################################################################
# That looks decent, but I think we can do better. Let's try 0.1 for 10 samples
# between the cross overs and the min/max

dn = 0.1
# 1/np.pi**2
n = np.arange(1, nn, step=dn)
xn = xx(n)

plot_f()
plt.show()


###############################################################################
# Now that looks pretty darn good! How about we try integrating :math:`f(x)` now!
# To do so, we simply take our values and multiply by the :math:`\Delta x` value
# (the rectangle widths). It's important to note here that :math:`\Delta x` is not a
# constant this time, so well need to compute an array of all of our
# :math:`\Delta x` values first.

dx = np.pi / (128 * 4)
x = np.arange(2 / np.pi, 2 * np.pi, step=dx)
right = np.sum(f(x) * dx)
right

###############################################################################
# The right side there is pretty good
# (`check with wolfram alpha <https://www.wolframalpha.com/input/?i=integrate+sin+1%2Fx+dx+from+x%3D2%2Fpi+to+2pi>`_)


def compute_left(dn, nn=1000):
    n = np.arange(1, nn, step=dn)
    xn = xx(n)
    dx = np.abs(np.diff(xn))
    return np.sum(f(xn)[:-1] * dx)


left = compute_left(dn)
left

###############################################################################
# Well that's not very good as we know the true value for the left side to be
# 0.164619 `from Wolfram Alpha <https://www.wolframalpha.com/input/?i=integrate+sin+1%2Fx+dx+from+x%3D0+to+2%2Fpi+>`_.
# Let's see if increasing the discretization helps.


left = compute_left(0.0001)
left


###############################################################################
left + right

###############################################################################
# The full integral is known to be 2.26277 from `Wolfram Alpha <https://www.wolframalpha.com/input/?i=integrate+sin+1%2Fx+dx+from+x%3D0+to+2pi>`_
# so that's not too bad of an approximation!
#
# And there you have it! The integral of :math:`\sin(\frac{1}{x})` has been
# numerically integrated!
