import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-xl text-sm font-medium ring-offset-background transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-pacific-400 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default:
          "bg-primary text-primary-foreground hover:bg-primary/90 shadow-sm hover:shadow-md active:scale-[0.98]",
        destructive:
          "bg-destructive text-destructive-foreground hover:bg-destructive/90 shadow-sm hover:shadow-md",
        outline:
          "border border-slate-200 bg-white/80 backdrop-blur-sm hover:bg-white hover:border-pacific-300 text-slate-700 hover:text-pacific-700",
        secondary:
          "bg-slate-100 text-slate-700 hover:bg-slate-200 shadow-sm",
        ghost:
          "hover:bg-white/60 hover:text-slate-900",
        link:
          "text-pacific-600 underline-offset-4 hover:underline",
        // Pacific Blue - main CTA
        pacific:
          "bg-gradient-to-b from-pacific-500 to-pacific-600 text-white shadow-lg shadow-pacific-500/25 hover:shadow-xl hover:shadow-pacific-500/30 hover:from-pacific-400 hover:to-pacific-500 active:scale-[0.98]",
        // Glass variant - Apple style
        glass:
          "glass-button text-slate-700 hover:text-slate-900 active:scale-[0.98]",
        "glass-pacific":
          "glass-pacific text-pacific-700 hover:text-pacific-800 active:scale-[0.98]",
        // Dark variant
        dark:
          "bg-slate-900 text-white shadow-lg hover:bg-slate-800 active:scale-[0.98]",
        // White variant for dark backgrounds
        white:
          "bg-white text-slate-900 shadow-lg shadow-black/10 hover:shadow-xl hover:bg-white/95 active:scale-[0.98]",
        // Subtle variant
        subtle:
          "bg-slate-100/80 text-slate-600 hover:bg-slate-200/80 hover:text-slate-900",
      },
      size: {
        default: "h-10 px-5 py-2",
        sm: "h-9 rounded-lg px-4 text-xs",
        lg: "h-12 rounded-xl px-8 text-base",
        xl: "h-14 rounded-2xl px-10 text-lg",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
