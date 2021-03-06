# LPR makefile, for cross-platform compilation & linking
# (c) Shahar Gino, June-2017, sgino209@gmail.com

AR		:=	ar
ifeq ($(shell uname -s), Darwin)
CXX		:=	clang++
CXXFLAGS	:=	-stdlib=libc++ -fpic -O3 -Wall -D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS -DNO_HISTOGRAM -std=c++11 \
                        -Wno-c++11-extensions -Wno-reorder -Wno-overloaded-virtual -Wno-null-conversion -Wno-delete-non-virtual-dtor -Wno-comment -Wno-format -Wno-char-subscripts
else
CXX		:=	g++
CXXFLAGS	:=	-fpic -O3 -Wall -DLUA_ENABLED -D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS -DNO_HISTOGRAM -std=c++11 \
                        -Wno-c++11-extensions -Wno-reorder -Wno-overloaded-virtual -Wno-null-conversion -Wno-delete-non-virtual-dtor -Wno-comment -Wno-format -Wno-char-subscripts
endif

LDFLAGS		:= 	-L/usr/local/lib -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_imgcodecs -lopencv_ml -lopencv_video -lopencv_text -lcurses `pkg-config --libs tesseract`

INC		:= 	-I/usr/local/lib \
    			-I/usr/local/include \
			-I~/opencv/** \
			-I./

MODULES		:=	DetectChars \
			DetectPlates \
                        LPR_wrapper \
                        Main \
                        PossibleChar \
                        Preprocess \
                        Auxiliary \
			onvif_capture

LIB_NAME	:=	lpr.a

EXEC_NAME	:=	lpr

BUILD		:=	build

EXECUTABLE	:=	$(BUILD)/$(EXEC_NAME)

LIB		:=	$(BUILD)/$(LIB_NAME)

OBJ		:=	$(patsubst %,$(BUILD)/%.o,$(MODULES))


$(EXECUTABLE) : $(LIB)
	$(CXX) $(LIB) $(LDFLAGS) -o $@

$(LIB) : $(BUILD) $(OBJ)
	$(AR) rcu $(LIB) $(OBJ)

$(BUILD)/%.o : %.cpp
	$(CXX) $(CXXFLAGS) $(INC) -c $< -o $@

$(BUILD):
	mkdir -p $(BUILD)

.PHONY: clean
clean:
	rm -f $(LIB)
	rm -f $(OBJ)

.PHONY: clobber
clobber:
	rm -rf $(BUILD)


