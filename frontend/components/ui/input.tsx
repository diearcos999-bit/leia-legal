import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const inputVariants = cva(
  "flex w-full rounded-md border bg-background text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200",
  {
    variants: {
      variant: {
        default:
          "h-10 border-input px-3 py-2 focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
        hero:
          "h-14 md:h-16 border-pacific-200 px-5 py-4 text-base md:text-lg shadow-hero-input focus-visible:ring-2 focus-visible:ring-pacific-400 focus-visible:border-pacific-400 hover:border-pacific-300 hover:shadow-lg",
        "hero-lg":
          "h-16 md:h-20 border-pacific-200 px-6 py-5 text-lg md:text-xl shadow-hero-input focus-visible:ring-2 focus-visible:ring-pacific-400 focus-visible:border-pacific-400 hover:border-pacific-300 hover:shadow-lg rounded-xl",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement>,
    VariantProps<typeof inputVariants> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, variant, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(inputVariants({ variant, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"

export { Input, inputVariants }
