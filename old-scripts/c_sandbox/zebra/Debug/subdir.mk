################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../autoplay.c \
../bitbcnt.c \
../bitbmob.c \
../bitboard.c \
../bitbtest.c \
../cntflip.c \
../counter.c \
../display.c \
../doflip.c \
../end.c \
../epcstat.c \
../error.c \
../eval.c \
../game.c \
../getcoeff.c \
../globals.c \
../hash.c \
../main.c \
../midgame.c \
../moves.c \
../myrandom.c \
../opname.c \
../osfbook.c \
../patterns.c \
../pcstat.c \
../probcut.c \
../safemem.c \
../search.c \
../stable.c \
../testa.c \
../thordb.c \
../timer.c \
../unflip.c 

OBJS += \
./autoplay.o \
./bitbcnt.o \
./bitbmob.o \
./bitboard.o \
./bitbtest.o \
./cntflip.o \
./counter.o \
./display.o \
./doflip.o \
./end.o \
./epcstat.o \
./error.o \
./eval.o \
./game.o \
./getcoeff.o \
./globals.o \
./hash.o \
./main.o \
./midgame.o \
./moves.o \
./myrandom.o \
./opname.o \
./osfbook.o \
./patterns.o \
./pcstat.o \
./probcut.o \
./safemem.o \
./search.o \
./stable.o \
./testa.o \
./thordb.o \
./timer.o \
./unflip.o 

C_DEPS += \
./autoplay.d \
./bitbcnt.d \
./bitbmob.d \
./bitboard.d \
./bitbtest.d \
./cntflip.d \
./counter.d \
./display.d \
./doflip.d \
./end.d \
./epcstat.d \
./error.d \
./eval.d \
./game.d \
./getcoeff.d \
./globals.d \
./hash.d \
./main.d \
./midgame.d \
./moves.d \
./myrandom.d \
./opname.d \
./osfbook.d \
./patterns.d \
./pcstat.d \
./probcut.d \
./safemem.d \
./search.d \
./stable.d \
./testa.d \
./thordb.d \
./timer.d \
./unflip.d 


# Each subdirectory must supply rules for building sources it contributes
%.o: ../%.c
	@echo 'Building file: $<'
	@echo 'Invoking: Cross GCC Compiler'
	gcc -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


